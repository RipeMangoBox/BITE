---
title: "InstAP: Instance-Aware Vision-Language Pre-Train for Spatial-Temporal Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/InstAP_Instance_Aware_Vision_Language_Pre_Train_for_Spatial_Temporal_Understanding.pdf
project_link: null
code_link: null
aliases:
- InstAP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将实例级对比对齐 (instance-level contrastive alignment) 加入预训练损失，强制模型同时学习全局场景和细粒度实例-文本对应关系。
primary_logic: 实例级理解必须作为预训练的核心特性，而非附加任务；通过联合优化全局和实例感知的对齐目标，模型可以同时提升细粒度定位和整体场景理解能力。
claims:
- 在相同的训练数据下，InstAP大幅超越仅使用全局描述或全局化实例描述的UMT-L基线（例如在InstVL-10K (img)上，T2V R@1 44.05 vs 34.83），验证了实例感知对齐机制的核心贡献。
- 在MSR-VTT和DiDeMo上达到新的零样本检索最先进水平，同时超越了原始UMT-L，表明实例感知不仅未损害全局性能，反而提升了全局理解。
- 在视频定位上IoU@90大幅提升，从14.44提高到25.13，证明实例感知预训练目标有效编码了精确的时空坐标信息。
- InstVL-10K (img) instance 上 T2V R@1 = 44.05
---

# InstAP: Instance-Aware Vision-Language Pre-Train for Spatial-Temporal Understanding

> [!tip] 核心洞察
> 实例级理解必须作为预训练的核心特性，而非附加任务；通过联合优化全局和实例感知的对齐目标，模型可以同时提升细粒度定位和整体场景理解能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | InstAP：面向时空理解的实例感知视觉语言预训练 |
| 英文题名 | InstAP: Instance-Aware Vision-Language Pre-Train for Spatial-Temporal Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.08337) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InstAP |
| Dataset | InstVL-10K (img) instance, InstVL-1K (video) instance, InstVL-1K (img) global, InstVL-1K (video) grounding |

> [!tip] 效果简介
> - InstVL-10K (img) instance 上，T2V R@1 44.05 vs 34.83 (UMT-L g+i) (+9.22)。
> - InstVL-1K (video) instance 上，T2V R@1 60.63 vs 40.38 (UMT-L g+i) (+20.25)。
> - InstVL-1K (img) global 上，T2V R@1 99.20 vs 96.20 (UMT-L g+i) (+3.00)。

## 概述

当前视觉语言预训练（VLP）框架普遍依赖全局视频-文本对齐，缺乏实例级监督，导致模型无法精确识别和区分文本中提到的特定对象或实体。这一瓶颈在需要细粒度时空理解的场景（如视频中特定实例的检索与定位）中尤为突出。

**InstAP** 提出将实例感知直接嵌入预训练阶段，引入实例级对比对齐目标，强制模型同时学习全局场景语义和细粒度实例-文本对应关系。其核心洞察在于：实例级理解不应是附加任务，而应作为预训练的核心特性，通过联合优化全局和实例感知的对齐目标，同时提升细粒度定位与整体场景理解能力。

在公平的训练数据对比下，InstAP 大幅超越仅使用全局描述或全局化实例描述的 **UMT-L**（Li et al., ICCV 2023）基线。例如，在 InstVL-10K (img) 实例检索上，T2V R@1 从 34.83 提升至 44.05（+9.22），验证了实例感知对齐机制的核心贡献。在标准零样本文本-视频检索基准上，InstAP 在 MSR-VTT（R@1 41.1）和 DiDeMo（R@1 54.0）上达到新的最优水平，同时超越了原始 UMT-L，表明实例感知不仅未损害全局性能，反而增强了全局理解。在视频定位任务上，IoU@90 从 14.44 大幅提升至 25.13，证实预训练目标有效编码了精确的时空坐标信息。

方法上，InstAP 在 **UMT-L** 的掩码视频建模与全局对齐基础上，新增了两个关键设计：一是从检测器生成的轨迹/区域裁剪 RoI 特征，通过交叉注意力融合全局上下文得到实例感知嵌入；二是在损失函数中增加实例级对比损失、匹配损失和掩码语言建模损失，并采用同视频内负样本掩码避免假阴性。完整训练损失为重建损失、全局对齐损失与实例感知对齐损失之和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{global}} + \mathcal{L}_{\mathrm{inst}}$$

消融实验进一步证实，增加实例感知损失后，视频实例检索平均召回从 57.71 提升至 75.32；可学习的实例温度参数和轨迹数据集的引入均带来显著增益。

## 背景与动机

### 视觉语言预训练的全局对齐瓶颈

视觉语言预训练（VLP）已成为多模态理解的基础范式，其核心目标是通过大规模图文/视频-文本数据学习通用视觉表征。当前主流的VLP框架——包括CLIP系列、**UMT**（Li et al., ICCV 2023）、**VideoPrism**（Zhao et al., 2024）等——几乎完全依赖**全局视频-文本对齐**：模型学习将整段视频与整句描述在共享嵌入空间中拉近。这种全局粒度的监督信号虽然支撑了零样本检索等任务，却存在一个根本性缺陷：**模型无法精确识别和区分文本中提到的特定对象或实体**。

具体而言，当一段视频包含多个实例（如"穿红裙子的女人"和"持相机的男人"），而文本描述仅提及其中一个时，全局对齐机制只能将整段视频与整句文本匹配，缺乏将文本片段精确锚定到对应视觉区域的能力。这使得模型在面对细粒度查询时，容易被语义干扰项混淆——例如，将"白色汽车"错误匹配到场景中另一辆外观相似的车辆。

### 实例级监督的缺失与现有方案的局限

部分工作尝试通过后处理或附加任务引入细粒度理解能力，例如在预训练完成后进行视觉定位微调，或利用目标检测特征作为辅助输入。然而，这些方案存在两个共同问题：

1. **实例理解被视为附加任务而非预训练核心特性**：模型在预训练阶段未接触实例级对齐信号，导致其底层视觉表征缺乏精确的实体区分能力。后续微调只能在已有表征基础上做有限补偿。
2. **全局性能与细粒度能力难以兼顾**：当模型被强制学习实例级信息时，往往以牺牲全局场景理解为代价。例如，**UMT-L**在仅使用全局描述的数据上训练时，其在标准检索基准上的表现优于使用混合粒度数据的变体，表明不恰当的实例监督可能损害整体性能。

### InstAP的核心动机

本文的核心洞察是：**实例级理解必须作为预训练的核心特性，而非附加任务**。为此，InstAP提出将实例感知对比对齐直接嵌入预训练阶段，通过联合优化全局和实例感知的对齐目标，使模型同时学习全局场景语义和细粒度实例-文本对应关系。

这一设计的关键因果机制在于：实例感知对齐迫使模型将文本中的实体提及（如"the woman in red"）与视觉中的特定时空区域（如该女性对应的轨迹RoI特征）进行精确匹配，从而在表征空间中形成可区分的实例级嵌入。与此同时，全局对齐分支保留了场景整体理解能力，避免细粒度学习对全局性能的侵蚀。

### 数据层面的支撑：InstVL数据集

为支撑实例感知预训练，本文构建了**InstVL**数据集，其核心特点是**双粒度文本标注**：每个视觉样本同时配备一个全局场景描述和一组实体锚定的轨迹实例描述。这种数据组织形式使得模型在训练时能够同时接收全局和实例级监督信号，为联合优化目标提供了必要的数据基础。

## 核心创新

### 瓶颈诊断：全局对齐的粒度缺失

当前视觉语言预训练（VLP）框架的核心瓶颈在于**仅依赖全局视频-文本对齐**，缺乏实例级监督信号。以强基线 **UMT-L**（Li et al., ICCV 2023）为例，其训练目标只包含视频级对比损失、视频-文本匹配损失和掩码语言建模损失，模型被迫将所有视觉信息压缩为单一全局表征。这种设计导致两个关键缺陷：

1. **实例混淆**：模型无法精确识别文本中提到的特定对象或实体，当场景中存在多个语义相似实例时（如“穿红色衬衫的男子”与“穿蓝色衬衫的男子”），全局表征难以区分。
2. **定位能力缺失**：全局对齐不编码任何空间-时间坐标信息，导致模型在需要精确区域定位的下游任务（如视觉定位）上表现极差。

### 因果调控变量：实例级对比对齐

InstAP 的核心创新是将**实例级对比对齐**（instance-level contrastive alignment）直接嵌入预训练损失函数，作为与全局对齐并列的第一性目标。具体而言，模型不再仅学习“整个视频对应整段描述”，而是强制学习“文本中的每个实体短语对应视频中的特定时空区域”。

这一因果调控通过两个 **changed slots** 实现：

| 变更维度 | 基线（UMT-L） | InstAP |
|---------|-------------|--------|
| **损失函数** | 仅含 $\mathcal{L}_{\text{VTC}}$、$\mathcal{L}_{\text{VTM}}$、$\mathcal{L}_{\text{MLM}}$ 全局损失 | 新增实例级对比损失 $\mathcal{L}_{\text{VTC}}^{\text{inst}}$、实例级匹配损失 $\mathcal{L}_{\text{VTM}}^{\text{inst}}$、实例级掩码语言建模损失 $\mathcal{L}_{\text{MLM}}^{\text{inst}}$，并采用同视频内负样本掩码 $\alpha_{n,m}$ 避免假阴性 |
| **视觉编码器输入** | 仅使用全帧视频特征（全局池化） | 从检测器生成的轨迹/区域裁剪 RoI 特征，通过交叉注意力融合全局上下文得到实例感知嵌入 |

### 实例感知对齐机制

实例嵌入的生成是方法的关键工程创新（Figure 3）。给定检测器输出的轨迹区域，Trajectory RoI Encoder $f_\theta$ 提取实例级视觉特征作为 Query $\mathbf{Q}$，同时以全局视频特征作为 Key $\mathbf{K}$ 和 Value $\mathbf{V}$，通过注意力池化（Attention Pool）进行交叉注意力融合：

$$\mathbf{z}_n = \text{AttentionPool}(\mathbf{Q}_n, \mathbf{K}, \mathbf{V})$$

这一设计的精妙之处在于：实例嵌入并非孤立的局部特征，而是**注入了全局上下文信息的实例感知表征**——它既知道“自己是谁”（局部外观），也知道“自己在哪”（全局场景关系）。

实例级对比损失的形式化定义体现了对假阴性问题的审慎处理：

$$\mathcal{L}_{\text{VTC}}^{\text{inst}} = -\frac{1}{N}\sum_{n=1}^{N} \log \frac{\exp(\tilde{\mathbf{z}}_n^{\top}\tilde{\mathbf{s}}_n/\tau_{\text{inst}})}{\sum_{m=1}^{N} \alpha_{n,m} \exp(\tilde{\mathbf{z}}_n^{\top}\tilde{\mathbf{s}}_m/\tau_{\text{inst}})}$$

其中 $\alpha_{n,m}$ 为同视频负样本掩码：当第 $n$ 个实例与第 $m$ 个实例来自同一视频且语义相似时，$\alpha_{n,m}=0$，防止模型将语义相近的同视频实例错误地推开。此外，采用**可学习的实例温度参数** $\tau_{\text{inst}}$（而非共享全局温度）带来显著提升（+8.09 on InstVL-1K img），表明实例级对比需要不同于全局对比的判别粒度。

### 完整训练范式

最终训练损失将自监督重建、全局对齐和实例感知对齐统一为联合优化目标：

$$\mathcal{L} = \mathcal{L}_{\text{rec}} + \mathcal{L}_{\text{global}} + \mathcal{L}_{\text{inst}}$$

其中 $\mathcal{L}_{\text{rec}}$ 为掩码视频建模中的教师-学生特征回归损失（Eq. 1），$\mathcal{L}_{\text{global}}$ 包含全局 VTC、VTM、MLM 三项损失，$\mathcal{L}_{\text{inst}}$ 为对应的实例级版本。这种设计确保了实例感知不是附加任务，而是预训练的核心特性——模型在从零开始学习视觉表征时，就同时建立全局场景理解和细粒度实例-文本对应两种能力。

### 与现有工作的本质差异

现有细粒度视觉语言工作（如基于 **CLIP4Clip** 的区域匹配或 **SigLIP** 的密集对齐）通常将实例理解作为后处理步骤或微调阶段的附加模块。InstAP 的根本不同在于：**实例感知是预训练损失函数的内生组成部分**，而非事后嫁接。这解释了为何在完全相同的训练数据下，InstAP 大幅超越仅使用全局描述或全局化实例描述的 UMT-L 基线（例如 InstVL-10K (img) 上 T2V R@1 44.05 vs 34.83），差距源于实例感知对齐机制本身，而非数据量的增加。

## 整体框架

InstAP 的整体设计围绕一个核心命题展开：**实例级理解不应是预训练后的附加任务，而应作为预训练阶段的内在特性**。为此，框架将全局场景对齐与细粒度实例感知对齐统一在一个端到端的联合优化目标下，形成“全局-局部”双支路协同的预训练范式。

### 框架总览

如 Figure 1 右侧所示，InstAP 的 pipeline 由三个关键阶段串联而成：

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual overview of the InstAP framework and InstVL dataset. Left: InstVL features dual-granularity video annotations: holistic Global Captions and entity-grounded Trajectory Instance Captions. Right: InstAP fuses global and instance-level features via Global-Local Cross Attention, optimizing through joint Global and Instance-Aware Alignment objectives*

1. **掩码视频建模编码器**：通过教师-学生框架进行自监督时空掩码重建，为后续对齐提供强视觉表征。
2. **全局视觉-文本对齐**：在视频级粒度上执行标准的对比学习（VTC）、视频-文本匹配（VTM）和掩码语言建模（MLM），捕获场景级语义对应。
3. **实例感知对齐模块**：从检测器生成的轨迹/区域中裁剪 RoI 特征，经全局-局部交叉注意力融合全局上下文，形成实例感知嵌入，再与文本中的实体描述进行实例级对比、匹配和 MLM。

三个阶段的损失函数以加和形式统一为完整训练目标：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{global}} + \mathcal{L}_{\mathrm{inst}}$$

其中 $\mathcal{L}_{\mathrm{global}}$ 包含全局 VTC、VTM 和 MLM 三项损失，$\mathcal{L}_{\mathrm{inst}}$ 则包含对应的实例级版本。

### 数据基础：InstVL 的双粒度标注

框架的有效性高度依赖训练数据的结构设计。InstVL 数据集为每个视频样本提供**双粒度文本标注**（Figure 1 左侧、Figure 2）：

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of our InstVL dataset. We display sampled frames with color-coded, temporally-consistent instance trajectories (e.g., ID: 0, ID: 1). The top text provides the fine-grained instance captions grounded to these trajectories; the bottom text provides the holistic global caption for the entire scene*

- **全局描述**：覆盖整个场景的 holistic caption。
- **轨迹实例描述**：与特定时空轨迹（trajectory）绑定的实体级描述，每条描述精确指向一个被持续跟踪的实例（如“dubai plate 61062”）。

这种双粒度标注使得模型在训练时能够同时接收场景级和实例级监督信号，是实现联合优化的数据前提。

### 视觉编码：掩码视频建模

视觉编码器采用教师-学生框架进行掩码视频建模，核心操作为**注意力引导的掩码策略**：计算每个 token 被其他 token 关注的平均注意力得分，选择得分最低的 token 进行掩码（掩码率 80%）。学生模型在可见 token 上回归教师模型的归一化特征，重建损失为余弦距离：

$$\mathcal{L}_{\mathrm{rec}} = \frac{1}{|\Omega|} \sum_{l \in \Omega} \left\| \frac{\mathbf{h}_l^{S}}{\|\mathbf{h}_l^{S}\|_2} - \frac{\mathbf{h}_l^{T}}{\|\mathbf{h}_l^{T}\|_2} \right\|_2^2$$

这一阶段不依赖文本，纯粹通过自监督方式建立时空视觉表征。

### 全局对齐支路

在掩码建模的基础上，全局对齐支路执行三项标准 VLP 任务：

- **视频-文本对比（VTC）**：将视频级池化特征 $\tilde{\mathbf{v}}$ 与文本池化特征 $\tilde{\mathbf{t}}$ 进行双向 InfoNCE 对比，使匹配对在嵌入空间中靠近。
- **视频-文本匹配（VTM）**：通过融合 Transformer（BERT）对视频-文本对进行二分类，判断是否匹配。
- **掩码语言建模（MLM）**：以视频特征为条件，预测文本中被掩码的 token。

这三项损失的联合优化使模型获得场景级的跨模态对齐能力。

### 实例感知对齐支路

这是 InstAP 的核心创新，其关键设计在于**实例嵌入的构造方式**（Figure 3）：

1. **轨迹 RoI 编码器**：从检测器（GroundingDINO）和跟踪器（SAM2）生成的时空轨迹中裁剪区域特征，作为实例查询 $\mathbf{Q}$。
2. **全局-局部交叉注意力**：将实例查询 $\mathbf{Q}$ 与全局视频特征 $\mathbf{K}, \mathbf{V}$ 进行注意力池化，使实例嵌入融合全局上下文信息，避免因裁剪区域过小而丢失语义。
3. **实例级对比损失**：将融合后的实例嵌入 $\tilde{\mathbf{z}}$ 与对应的文本实体嵌入 $\tilde{\mathbf{s}}$ 进行对比。该损失的关键改进在于**同视频内负样本掩码**：同一视频内的多个实例描述可能描述不同实体，但也可能因语义相近而构成假阴性，因此通过掩码矩阵 $\alpha_{n,m}$ 排除同视频内的潜在假阴性对：

$$\mathcal{L}_{\mathrm{VTC}}^{\mathrm{inst}} = -\frac{1}{N}\sum_{n=1}^{N} \log \frac{\exp(\tilde{\mathbf{z}}_n^{\top}\tilde{\mathbf{s}}_n/\tau_{\mathrm{inst}})}{\sum_{m=1}^{N} \alpha_{n,m} \exp(\tilde{\mathbf{z}}_n^{\top}\tilde{\mathbf{s}}_m/\tau_{\mathrm{inst}})}$$

此外，实例支路同样包含对应的 VTM 和 MLM 损失，形成完整的实例级对齐目标族。

### 输入输出流总结

| 阶段 | 输入 | 输出 | 核心损失 |
|------|------|------|----------|
| 掩码视频建模 | 8帧 224×224 视频片段 | 时空视觉 token 序列 | $\mathcal{L}_{\mathrm{rec}}$ |
| 全局对齐 | 视频 token + 全局描述文本 | 视频级嵌入、融合特征 | $\mathcal{L}_{\mathrm{VTC}} + \mathcal{L}_{\mathrm{VTM}} + \mathcal{L}_{\mathrm{MLM}}$ |
| 实例感知对齐 | RoI 裁剪特征 + 全局上下文 + 实例描述文本 | 实例感知嵌入 | $\mathcal{L}_{\mathrm{VTC}}^{\mathrm{inst}} + \mathcal{L}_{\mathrm{VTM}}^{\mathrm{inst}} + \mathcal{L}_{\mathrm{MLM}}^{\mathrm{inst}}$ |

三个阶段的输出通过联合损失 $\mathcal{L}$ 统一反向传播，使得视觉编码器在预训练过程中同时学习全局场景语义和细粒度实例-文本对应关系。消融实验（Table 4）证实，仅添加实例感知损失即可将 InstVL-1K 视频实例检索的平均召回从 57.71 提升至 75.32，验证了该支路的独立贡献。

## 核心模块与公式推导

### 3.1 掩码视频建模编码器

InstAP 的视觉编码器采用教师-学生自监督框架进行时空掩码重建，以学习强视觉表征。该模块对输入视频进行注意力引导的掩码处理：首先计算每个 token 的重要性分数 $\mathbf{s} = \frac{1}{L} \mathbf{A} \mathbf{1}$（其中 $\mathbf{A}$ 为注意力矩阵，$L$ 为 token 数），然后按给定掩码比 $\rho$ 选择分数最低的 $L_m = \lceil \rho L \rceil$ 个 token 进行掩码。学生网络处理掩码后的视频，教师网络处理完整视频，通过回归未掩码 token 的高层语义特征来驱动学习。

重建损失定义为学生与教师归一化特征之间的余弦距离：

$$
\mathcal{L}_{\mathrm{rec}} = \frac{1}{|\Omega|} \sum_{l \in \Omega} \left\| \frac{\mathbf{h}_l^{S}}{\|\mathbf{h}_l^{S}\|_2} - \frac{\mathbf{h}_l^{T}}{\|\mathbf{h}_l^{T}\|_2} \right\|_2^2
$$

其中 $\Omega$ 为可见 token 的索引集合，$\mathbf{h}_l^{S}$ 和 $\mathbf{h}_l^{T}$ 分别为学生和教师网络在第 $l$ 个 token 处的输出特征。该损失强制学生网络从部分观测中恢复与教师一致的语义表示，为后续的全局和实例级对齐提供高质量的视频特征基础。

### 3.2 全局视觉-文本对齐

全局对齐模块沿用经典 VLP 框架的三项损失函数，在视频级粒度上建立视觉与文本的对应关系。

**视频-文本对比损失（VTC）** 采用双向 InfoNCE 形式，将配对视频和文本的投影嵌入拉近，同时推开批次内其他样本：

$$
\mathcal{L}_{\mathrm{VTC}} = -\frac{1}{B}\sum_{i=1}^{B} \log \frac{\exp(\tilde{\mathbf{v}}_i^{\top}\tilde{\mathbf{t}}_i/\tau)}{\sum_{j=1}^{B}\exp(\tilde{\mathbf{v}}_i^{\top}\tilde{\mathbf{t}}_j/\tau)} - \frac{1}{B}\sum_{i=1}^{B} \log \frac{\exp(\tilde{\mathbf{t}}_i^{\top}\tilde{\mathbf{v}}_i/\tau)}{\sum_{j=1}^{B}\exp(\tilde{\mathbf{t}}_i^{\top}\tilde{\mathbf{v}}_j/\tau)}
$$

其中 $\tilde{\mathbf{v}}_i$ 和 $\tilde{\mathbf{t}}_i$ 分别为第 $i$ 个视频和文本的池化后投影嵌入，$\tau$ 为可学习温度参数，$B$ 为批次大小。

**视频-文本匹配损失（VTM）** 通过二元交叉熵判断视频与文本是否匹配：

$$
\mathcal{L}_{\mathrm{VTM}} = -\frac{1}{B}\sum_{i=1}^{B} \bigl[ y_i \log p_i + (1 - y_i) \log (1 - p_i) \bigr]
$$

其中 $p_i$ 为融合 Transformer（BERT）输出的匹配概率，$y_i \in \{0,1\}$ 为真实标签。

**掩码语言建模损失（MLM）** 以视频特征为条件预测被掩码的文本 token：

$$
\mathcal{L}_{\mathrm{MLM}} = -\frac{1}{B}\sum_{i=1}^{B}\frac{1}{|M_i|}\sum_{j \in M_i} \log P(w_{i,j} \mid \mathbf{V}_i, \mathbf{T}_{i,\backslash M_i})
$$

其中 $M_i$ 为第 $i$ 个文本中被掩码的 token 索引集合，$\mathbf{V}_i$ 为视频特征，$\mathbf{T}_{i,\backslash M_i}$ 为可见文本 token。全局对齐总损失为 $\mathcal{L}_{\mathrm{global}} = \mathcal{L}_{\mathrm{VTC}} + \mathcal{L}_{\mathrm{VTM}} + \mathcal{L}_{\mathrm{MLM}}$。

### 3.3 实例感知对齐模块

实例感知对齐是 InstAP 的核心创新，其关键设计在于通过 Trajectory RoI 编码器与全局-局部交叉注意力机制，将检测器生成的区域/轨迹特征转化为实例感知嵌入，并在实例级粒度上进行对比、匹配和掩码语言建模。

**实例嵌入生成**：如 Figure 3 所示，Trajectory RoI 编码器 $f_\theta$ 从检测器裁剪的区域中提取实例查询特征 $\mathbf{Q}$，随后通过交叉注意力与全局视频上下文（$\mathbf{K}, \mathbf{V}$）进行 Attention Pooling 融合，得到包含全局上下文信息的实例感知嵌入 $\mathbf{z}_n$。这一设计使实例特征既能保留局部细节，又能感知整体场景语义。

**实例级对比损失（$\mathcal{L}_{\mathrm{VTC}}^{\mathrm{inst}}$）** 是实例对齐的核心，其关键创新在于同视频负样本掩码机制，避免将同一视频内的其他正例实例误当作负样本：

$$
\mathcal{L}_{\mathrm{VTC}}^{\mathrm{inst}} = -\frac{1}{N}\sum_{n=1}^{N} \log \frac{\exp(\tilde{\mathbf{z}}_n^{\top}\tilde{\mathbf{s}}_n/\tau_{\mathrm{inst}})}{\sum_{m=1}^{N} \alpha_{n,m} \exp(\tilde{\mathbf{z}}_n^{\top}\tilde{\mathbf{s}}_m/\tau_{\mathrm{inst}})}
$$

其中 $\tilde{\mathbf{z}}_n$ 为第 $n$ 个实例的视觉嵌入，$\tilde{\mathbf{s}}_n$ 为对应实例描述的文本嵌入，$\tau_{\mathrm{inst}}$ 为实例级可学习温度参数。掩码系数 $\alpha_{n,m}$ 在实例 $n$ 和 $m$ 来自同一视频时设为 0，否则为 1，有效消除了假阴性干扰。消融实验表明，可学习实例温度带来显著提升（InstVL-1K img 上 +8.09），而同视频负样本掩码是实例对比成功的关键。

**实例级匹配与 MLM**：类似全局对齐，实例嵌入同样参与 VTM 和 MLM 损失计算，形成 $\mathcal{L}_{\mathrm{inst}} = \mathcal{L}_{\mathrm{VTC}}^{\mathrm{inst}} + \mathcal{L}_{\mathrm{VTM}}^{\mathrm{inst}} + \mathcal{L}_{\mathrm{MLM}}^{\mathrm{inst}}$。

### 3.4 联合训练目标

InstAP 的完整训练损失为三项目标的加权组合：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{global}} + \mathcal{L}_{\mathrm{inst}}
$$

该联合优化策略使模型在预训练阶段同时学习全局场景语义和细粒度实例-文本对应关系。实验证明，这种设计不仅未损害全局理解能力，反而使 InstAP 在 MSR-VTT 和 DiDeMo 上超越原始 UMT-L 基线，同时在实例检索和视觉定位任务上取得大幅提升——这验证了实例感知作为预训练核心特性而非附加任务的设计理念。

### 补充图表

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/003_Figure_3.jpg]]
*Figure 3: Our instance-aware alignment mechanism. Instance features (Query Q) from a Trajectory RoI Encoder (fθ) are fused with global context (Key K, Value V ) via an Attention Pool to create an instance-aware embedding. This embedding is contrasted with text features*

## 实验与分析

### 核心实验设置

InstAP 基于 **UMT-L**（Li et al., ICCV 2023）的教师-学生掩码视频建模框架构建。预训练分两阶段进行：第一阶段在 320 块 NVIDIA H100 GPU 上训练 800 个 epoch，使用 8 帧 224×224 视频片段，AdamW 优化器（学习率 $1.5 \times 10^{-4}$），batch size 64，注意力引导的掩码率为 80%；对齐阶段在 200 块 B200 GPU 上训练 15 个 epoch。

为确保公平对比，所有基线模型均使用完全相同的训练语料库（InstVL）重新训练。关键基线包括：
- **UMT-L (InstVL; g)**：仅使用全局描述训练
- **UMT-L (InstVL; g+i)**：将全部描述（包括实例描述）当作全局描述训练，但不具备实例感知对齐机制

### 主结果：实例级检索

Table 1 展示了 InstAP 在 InstVL 基准上的核心性能。在实例级检索任务上，InstAP 展现出压倒性优势：

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/004_Table_1.jpg]]
*Table 1: Comparison of SOTA models and our InstAP on the InstVL test set. We report T2V/V2T R@1 on the instance and global splits across InstVL(img), InstVL(img-zero), and InstVL(video). UMT-L (InstVL; g/g+i) baselines use the same full training corpus as InstAP, trained with only InstVL’s global captions (g) or with all InstVL captions treated as global (g+i)*

- **InstVL-10K (img) 实例检索**：InstAP 的 T2V R@1 达到 **44.05**，相比 UMT-L (g+i) 的 34.83 提升 **+9.22** 个点。这一差距尤为关键，因为两者训练数据完全相同，直接验证了实例感知对齐机制的核心贡献——性能提升并非来自更密集的标注数据，而是来自框架本身。
- **InstVL-1K (video) 实例检索**：T2V R@1 从 40.38 跃升至 **60.63**，提升幅度高达 **+20.25** 个点。视频场景中时空轨迹信息的引入使得实例感知的优势更为显著。
- **InstVL-1K (img) 全局检索**：即使在全图级别的全局检索上，InstAP 仍达到 **99.20** 的 T2V R@1，超过 UMT-L (g+i) 的 96.20，表明实例感知不仅未损害全局理解，反而带来了正向迁移。

在分布偏移测试（InstVL img-zero，完全来自 COYO，与训练集 LAION 分布不同）中，InstAP 同样保持显著优势（T2V R@1 达到 47.00 vs. UMT-L g+i 的 36.30），验证了模型的泛化能力。

### 零样本文本-视频检索

Table 2 展示了在标准检索基准上的零样本性能。InstAP 在 **MSR-VTT** 上达到 R@1 **41.1**，在 **DiDeMo** 上达到 **54.0**，均创下新的最先进水平。值得注意的是，引入实例感知对齐后，InstAP 不仅没有出现全局性能退化，反而超越了原始 UMT-L 在 MSR-VTT 和 DiDeMo 上的表现，在其他数据集上保持竞争力。这表明实例级和全局级理解可以协同增强。

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/005_Table_2.jpg]]
*Table 2: Zero-shot text-to-video retrieval (R@1 / R@5 / R@10) on standard benchmarks. UMT-L (InstVL; g) and UMT-L (InstVL; g+i) are baselines trained on the full corpus as InstAP*

### 视觉定位

Table 3 报告了 InstVL-1K 上的视觉定位指标。InstAP 在所有 IoU 阈值上显著超越 UMT-L 基线，尤其在最具挑战性的视频分割上，**IoU@90 从 14.44 提升至 25.13**（+10.69 个点）。这一结果确认了实例感知预训练目标能够将精确的时空坐标信息有效编码进视觉特征中，而非仅在检索任务中发挥作用。

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/006_Table_3.jpg]]
*Table 3: Grounding metrics (IoU@{50, 70, 90}) on InstVL-1K*

定位任务采用 3 层 MLP 边界框回归头，附加在预训练编码器的融合视觉-文本特征之上，使用 L1 和 GIoU 损失进行微调。

### 消融分析

**实例感知损失的核心作用**（Table 4）：在基线模型上添加实例感知损失后，InstVL-1K (video) 实例检索的平均召回率从 57.71 提升至 **75.32**，提升幅度达 17.61 个点。这一消融直接量化了实例对齐目标的贡献。

**组件消融**（Table 5）揭示了各设计选择的影响：
- **可学习的实例温度参数**：相比共享全局温度，使用独立的可学习实例温度在 InstVL-1K (img) 上带来 **+8.09** 的显著提升，表明实例级对比需要不同的温度尺度来适应其特有的正负样本分布。
- **视频轨迹数据**：添加 50K 视频轨迹数据集在 InstVL-1K (video) 上带来最大提升（**+16.35**），说明时空轨迹信息对视频实例理解至关重要。
- **长描述子采样**：作为有效的正则化器，防止模型对冗长实例描述的过拟合。

### 失败模式与局限性

尽管整体性能显著提升，InstAP 仍存在明确的失败模式：
- **多实例混淆**：在复杂场景中，模型可能将文本查询与错误的实例匹配，此类错误占全部错误的 **44.6%**，是最主要的失败来源。当多个语义相似的实例同时出现时，模型缺乏足够的判别能力来精确区分。
- **检测器依赖性**：实例感知对齐依赖预训练的 **GroundingDINO** 检测器和 **SAM2** 跟踪器生成伪标签，可能继承这些模型的检测错误和跟踪漂移，在遮挡或小目标场景下尤为明显。
- **长描述信息损失**：长描述的随机子采样策略虽然起到正则化作用，但可能丢弃关键的细粒度语义信息。

### 定性分析

**Figure 4** 的注意力可视化对比显示，InstAP 倾向于更精确地关注与描述相关的区域（如“dubai plate 61062”），而仅使用全局对齐的基线模型的注意力往往分散或错位。**Figure 5** 的检索案例进一步表明，InstAP 能一致地检索到正确的细粒度描述，而全局基线模型容易被语义干扰项混淆，导致查询匹配错误。这些定性证据与定量结果一致，共同支持实例感知机制在细粒度理解上的优势。

### 补充图表

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/007_Table_4.jpg]]
*Table 4: Effect of adding the instance-aware loss*

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/009_Table_5.jpg]]
*Table 5: Ablation of InstAP components on the InstVL instancelevel test sets. We report mean recall, averaged over R@1, R@5, and R@10 for both V2T and T2V retrieval*

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/010_Figure_4.jpg]]
*Figure 4: InstAP tends to attend more closely to caption-relevant regions (e.g., ‘dubai plate 61062’) than the global-only baseline [29], which often exhibits diffuse or misaligned attention*

![[assets/figures/papers/paper_list_l2397_https_arxiv_org_abs_2604_08337/figures/008_Figure_5.jpg]]
*Figure 5: InstAP consistently retrieves correct fine-grained descriptions, whereas the global baseline [29] is confounded by semantic distractors and mismatches the query*

## 方法谱系与知识库定位

InstAP 的核心贡献在于将**实例感知对齐**从下游任务的后处理提升为预训练阶段的基础目标，从而在视觉语言模型的谱系中开辟了一条介于纯全局对齐与全密集标注之间的中间路径。

### 与基线方法的关系

**UMT-L**（Li et al., ICCV 2023）是 InstAP 的直接技术底座。UMT-L 通过教师-学生框架下的掩码视频建模（MVM）学习强时空表征，并在预训练中仅使用全局视频-文本对比损失（VTC）、视频文本匹配（VTM）和掩码语言建模（MLM）。InstAP 完整继承了这一全局对齐框架，但在此基础上引入了**实例级对比损失** $\mathcal{L}_{\mathrm{VTC}}^{\mathrm{inst}}$、实例级匹配损失和实例级 MLM，形成了“重建 + 全局对齐 + 实例对齐”的三元联合优化目标（Eq. 13）。

关键的因果验证来自公平对比基线：UMT-L (InstVL; g) 仅使用 InstVL 数据集中的全局描述训练，UMT-L (InstVL; g+i) 则将实例描述也当作全局描述使用。两者与 InstAP 共享完全相同的训练语料，但 InstAP 在实例检索上大幅超越它们（例如 InstVL-10K (img) 上 T2V R@1 44.05 vs 34.83），这一差距直接归因于实例感知对齐机制本身，而非数据量的增加。

**VideoPrism**（Zhao et al., 2024）作为视频基础视觉编码器，代表了另一条技术路线——通过大规模视频-文本对比预训练获得强视觉骨干。InstAP 与 VideoPrism 的互补关系在于：前者提供实例感知的跨模态对齐能力，后者提供强视觉特征提取能力。论文中 InstAP 在零样本检索上达到了与 VideoPrism 可比甚至更优的性能（MSR-VTT R@1 41.1，DiDeMo R@1 54.0），同时额外具备实例级定位能力。

**CLIP4Clip**（Luo et al., Neurocomputing 2022）和 **SigLIP**（Zhai et al., ICCV 2023）代表了基于 CLIP 架构的视频检索范式，它们依赖图像级预训练权重迁移到视频域，缺乏原生的时空建模和实例感知能力。InstAP 通过掩码视频建模原生编码时空信息，并在预训练中直接注入实例监督，从根本上区别于这些迁移学习方案。

### 适用边界与能力定位

InstAP 的能力边界由其预训练目标直接决定：

1. **强项领域**：细粒度实例检索和视觉定位是 InstAP 的核心优势区。在 InstVL-1K (video) 实例检索上达到 60.63 T2V R@1，在视频定位上 IoU@90 从基线 14.44 提升至 25.13，证明实例感知目标有效编码了精确的时空坐标信息。

2. **保持领域**：全局场景理解不仅未被实例感知目标损害，反而有所提升。在 InstVL-1K (img) 全局检索上达到 99.20 T2V R@1，在 MSR-VTT 和 DiDeMo 上超越原始 UMT-L，表明联合优化产生了正向迁移。

3. **未充分验证领域**：论文主要评估集中在检索和基础定位任务上，对更复杂的时空推理任务（如视频问答、时序动作定位、因果关系推理）的泛化能力未充分验证。这是实例感知预训练能否成为通用视频理解基础的关键开放问题。

### 局限与开放问题

**已知局限**：

- **多实例混淆**：在复杂场景中，44.6% 的错误来自多实例混淆，表明当前实例感知机制在处理密集交互场景时仍有不足。
- **检测器依赖**：实例级伪标签依赖预训练的 GroundingDINO 检测器和 SAM2 跟踪器生成，模型可能继承这些上游模块的错误，形成误差传播链。
- **长描述信息损失**：为处理 InstVL 的长描述，需要子采样策略，这作为正则化器有效但可能引入信息损失。
- **计算成本**：预训练需要 800 epochs（320 NVIDIA H100 GPUs），对齐阶段在 200 B200 GPUs 上训练 15 epochs，计算门槛极高，限制了社区复现和迭代速度。

**开放问题**：

1. 实例感知预训练能否提升更复杂的视频理解任务（如视频问答、时序动作定位）？这决定了该方法的通用性边界。
2. 对更长视频序列或更密集交互场景，当前框架的可扩展性如何？44.6% 的多实例混淆率提示了扩展瓶颈。
3. 实例感知表征能否作为多模态大模型（MLLM）的视觉编码器，为 MLLM 提供更细粒度的视觉基座？
4. 如何进一步降低训练成本，使实例感知预训练更易被社区复现和改进？

## 原文 PDF

![[paperPDFs/CVPR_2026/InstAP_Instance_Aware_Vision_Language_Pre_Train_for_Spatial_Temporal_Understanding.pdf]]
