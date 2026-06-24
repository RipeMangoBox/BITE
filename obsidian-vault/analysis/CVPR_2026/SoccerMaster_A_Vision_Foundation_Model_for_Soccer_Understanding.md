---
title: "SoccerMaster: A Vision Foundation Model for Soccer Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SoccerMaster_A_Vision_Foundation_Model_for_Soccer_Understanding.pdf
project_link: "https://haolinyang-hlyang.github.io/SoccerMaster"
code_link: null
aliases:
- SoccerMaster
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 监督多任务预训练策略，在单一框架内联合优化空间感知和语义推理任务，并利用自动标注管线 SoccerFactory 提供大规模空间监督。
primary_logic: 通过共享的视觉编码器同时学习空间细节（场地几何、运动员位置）和时间动态语义（事件、评论文本对齐），使得一个模型可以胜任从检测到描述的多种足球理解任务，且仅需轻量微调即可适配下游应用。
claims:
- SoccerMaster 在预训练任务上大幅超越通用视觉基础模型和足球专用模型，运动员检测 AP@50 提升 22.4 点，事件分类准确率提升 11.9 点，视觉-语言对齐 top-1 从 4.0% 提升至 39.0%。
- 加入通过 SoccerFactory 自动生成的空间标注数据后，紧凑模型上的运动员检测 AP@50 提升 4.3 点，验证了自动标注对空间感知任务的有效性。
- 多任务预训练相比单任务训练，视觉-语言对齐 top-1 从 32.6% 升至 36.8%，但在容量有限的紧凑模型上牺牲了运动员检测性能；全尺寸模型则可以保持检测性能。
- 在下游任务（相机校准、多目标跟踪、评论生成）上，仅需简单微调即可达到最优或具有竞争力的结果，体现通用表征的迁移能力。
---

# SoccerMaster: A Vision Foundation Model for Soccer Understanding

> [!tip] 核心洞察
> 通过共享的视觉编码器同时学习空间细节（场地几何、运动员位置）和时间动态语义（事件、评论文本对齐），使得一个模型可以胜任从检测到描述的多种足球理解任务，且仅需轻量微调即可适配下游应用。

| 字段 | 内容 |
|------|------|
| 中文题名 | SoccerMaster：面向足球理解的视觉基础模型 |
| 英文题名 | SoccerMaster: A Vision Foundation Model for Soccer Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.11016) · [Project](https://haolinyang-hlyang.github.io/SoccerMaster) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SoccerMaster |
| Dataset | SoccerNet-GSR, Athlete Detection, Event Classification, Vision-Language Alignment |

> [!tip] 效果简介
> - SoccerNet-GSR 上，GS-HOTA 64.1 vs 61.5 (KIST-GSR) (+2.6)。
> - Athlete Detection (SoccerNet test) 上，AP@50 91.5 vs 69.1 (SigLIP2) (+22.4)。
> - Event Classification 上，Accuracy 77.2 vs 65.3 (MatchVision) (+11.9)。

## 概述

足球视频理解长期面临一个根本性瓶颈：现有方法依赖孤立的、任务特定的专家模型，无法在单一框架内统一精细空间感知（如运动员检测、场地注册）与高级语义推理（如事件分类、评论生成）。这种割裂导致通用表征缺失，模型难以高效迁移至下游任务。

SoccerMaster 是首个足球专用的视觉基础模型，其核心思路是通过**监督多任务预训练**，在共享的视觉编码器上同时学习空间细节（场地几何、运动员位置）和时间动态语义（事件、评论文本对齐）。为支撑这一训练范式，作者构建了 **SoccerFactory** 自动标注管线，从海量转播画面中生成大规模空间标注（约 2.7M 帧），与现有数据集整合形成约 7.45M 帧的预训练语料。模型架构在 ViT 基础上引入**交替时空注意力**：前若干层保持空间自注意力以提取帧内信息，后若干层加入时间注意力以捕捉跨帧运动动态，从而在统一前向传播中产出兼顾空间与语义的多粒度表征。

实验表明，SoccerMaster 在预训练任务上大幅超越通用视觉基础模型和足球专用模型：运动员检测 AP@50 提升 22.4 点，事件分类准确率提升 11.9 点，视觉-语言对齐 top-1 从 4.0% 跃升至 39.0%（Table 3）。仅需轻量微调，模型即可在下游的相机校准、多目标跟踪和评论生成任务上达到最优或极具竞争力的结果，验证了通用表征的迁移能力。消融实验进一步确认，SoccerFactory 自动标注使紧凑模型上的运动员检测 AP@50 提升 4.3 点（Table 7），而多任务联合训练相比单任务训练显著提升了视觉-语言对齐性能，尽管在容量受限模型上会牺牲部分检测精度，但在全尺寸模型上可消除这一权衡。

**方法定位**：SoccerMaster 属于监督多任务视觉基础模型，其预训练策略在方法谱系上区别于通用自监督模型（如 DINOv3）和通用视觉-语言模型（如 SigLIP 2），也不同于仅做语义对齐的足球专用模型（如 MatchVision）。它通过联合优化检测、关键点回归、分类和对比学习目标，将空间感知与语义推理统一于单一框架，为领域基础模型的构建提供了可复用的范式。

## 背景与动机

足球作为全球最受欢迎的运动之一，其海量的视频数据催生了对自动化视觉理解的巨大需求。从运动员检测与跟踪、场地注册、事件分类到评论生成，足球场景涉及的任务横跨精细空间感知与高层语义推理两个层面，且二者深度耦合——例如，准确识别“进球”事件不仅需要检测球员与球门的位置关系，还需理解动作序列的时序语义。

然而，现有足球视觉理解方法长期处于**任务孤立**的状态：空间感知任务（如检测、场地注册）依赖专用检测器，语义推理任务（如事件分类、评论生成）则使用独立的分类或视觉-语言模型。这些“专家模型”各自为战，无法共享表征，导致：

1. **表征碎片化**：每个任务需从头训练或微调独立模型，缺乏一个统一的视觉骨干来同时编码空间细节与语义上下文。
2. **数据利用低效**：空间感知任务需要大量精细标注（边界框、关键点），而语义任务依赖事件标签或文本对齐信号，两类数据难以在单一框架内协同发挥作用。
3. **迁移能力受限**：孤立模型习得的表征难以泛化至未见的足球理解任务，下游适配成本高。

通用视觉基础模型（如 **SigLIP 2**、**DINOv3**）虽具备一定的跨任务泛化性，但其预训练目标与足球领域的结构化需求存在根本性错配——通用模型擅长开放场景的语义识别，却缺乏对球场几何、运动员身份、事件时序等足球核心要素的精细建模能力。足球专用模型（如 **MatchVision**）尝试弥合这一差距，但仍局限于视觉-语言对齐等单一维度，未能覆盖空间感知任务。

本文的核心动机在于：**能否构建一个统一的足球视觉基础模型，通过大规模多任务预训练，同时掌握空间感知与语义推理能力，从而以单一框架支撑从检测到描述的全谱系足球理解任务？**

为实现这一目标，本文面临两个关键挑战：

- **数据瓶颈**：大规模空间标注（运动员框、场地关键点、线条）极度稀缺，人工标注成本高昂。
- **架构与训练策略**：如何设计一个既能提取帧内空间细节、又能建模跨帧运动语义的视觉编码器，并在多任务联合优化中平衡空间与语义目标？

针对上述挑战，本文提出 **SoccerMaster**——首个足球专用的视觉基础模型，并配套 **SoccerFactory** 自动标注管线以解决数据瓶颈。SoccerMaster 通过监督多任务预训练策略，在约 745 万帧的大规模数据集上联合优化运动员检测与识别、场地关键点与线条检测、事件分类和视觉-语言对齐四类任务，使得单一模型能够习得多粒度的足球表征，仅需轻量微调即可适配下游应用。

## 核心创新

SoccerMaster 的核心创新在于**通过监督多任务预训练，将精细空间感知与高层语义推理统一到单一视觉基础模型中**，从而打破现有足球理解系统依赖孤立专家模型的瓶颈。其创新路径可从三个“changed slots”来理解。

### 1. 预训练目标：从单任务孤立学习到多任务联合优化

现有方法通常为运动员检测、事件分类、视觉-语言对齐等任务分别训练专用模型（如 **MatchVision** 仅做语义对齐，**DINOv3** 仅做空间表征）。SoccerMaster 的关键转变在于**联合优化五项任务**：运动员检测与识别（角色+球衣号码）、场地关键点与线条检测、事件分类、以及视频-评论对比对齐。

联合训练的总损失为：

$${ \mathcal { L } } _ { \mathrm { t o t a l } } = \lambda _ { \mathrm { a } } { \mathcal { L } } _ { \mathrm { a } } + \lambda _ { \mathrm { k } } { \mathcal { L } } _ { \mathrm { k } } + \lambda _ { \mathrm { l } } { \mathcal { L } } _ { \mathrm { l } } + \lambda _ { \mathrm { e } } { \mathcal { L } } _ { \mathrm { e } } + \lambda _ { \mathrm { c o n } } { \mathcal { L } } _ { \mathrm { c o n } }$$

这一设计的核心洞察是：**共享视觉编码器同时学习场地几何细节和事件时序语义，使表征兼具空间精度与语义丰富性**。实验证据表明，多任务预训练使视觉-语言对齐 top-1 从单任务训练的 32.6% 提升至 36.8%（Table 12），验证了语义任务间存在正向迁移。但需注意，在紧凑模型变体上，运动员检测 AP@50 会因此下降 6.3 个百分点——这是一个**容量依赖的权衡**，全尺寸模型则可消除此退化。

### 2. 训练数据规模与来源：从人工标注到自动标注管线驱动的大规模空间监督

足球视觉领域长期受限于空间标注的高成本，导致预训练数据规模不足。SoccerMaster 引入 **SoccerFactory 自动标注管线**，从广播视频中生成大规模空间标注（约 2.7M 帧），使预训练数据总量达到约 7.45M 帧（Table 2）。

SoccerFactory 三阶段管线（Figure 2）的核心机制是：
- **场地注册**：通过关键点/线条检测与 PnL 模块建立图像-标准球场坐标的几何映射；
- **跟踪与识别**：检测→角色/球队分类→ReID 跟踪，形成运动员轨迹；
- **后处理精修**：SAM2 分割与多数投票保证时序一致性。

该管线本身在 SoccerNet-GSR 游戏状态重建任务上达到 GS-HOTA 64.1，超越挑战赛冠军 KIST-GSR 的 61.5（Table 1），证明其标注质量可靠。消融实验（Table 7）显示，加入 SoccerFactory 自动标注后，紧凑模型上的运动员检测 AP@50 提升 4.3 点，mAP 提升 7.3 点——这是**数据规模驱动空间感知能力提升**的直接证据。

### 3. 视觉编码器架构：从纯空间注意力到时空分离注意力

通用视觉基础模型（如 SigLIP 2、DINOv3）使用标准 ViT，每帧独立处理，缺乏时序建模。SoccerMaster 的编码器设计为：前 $L_s$ 层保持空间自注意力，后 $L_{st}$ 层引入交替的时空注意力（TimeSformer 式）：

- **空间自注意力**：每个 token 仅与同一帧的 token 交互，提取帧内空间信息；
- **时间注意力**：每个 token 仅与同一空间位置的不同帧 token 交互，捕捉运动动态。

这一设计的因果机制是：**浅层保留细粒度空间细节，深层融合时序运动信息**，使得同一编码器能同时服务于检测（需要空间精度）和事件分类（需要动态理解）。在预训练任务对比中（Table 3），SoccerMaster 以冻结编码器+可训练任务头的方式，在运动员检测（AP@50 91.5 vs. SigLIP2 69.1）和事件分类（准确率 77.2 vs. MatchVision 65.3）上均大幅超越专用模型，证明时空分离设计有效避免了空间与语义表征的冲突。

### 创新总结

三个 changed slots 构成一个**协同创新体系**：自动标注管线提供大规模空间监督，时空编码器提供多粒度表征能力，多任务联合优化使两者相互增强。最终表现为：一个模型仅需轻量微调，即可在相机校准（FS 86.8 vs. PnlCalib 78.6）、多目标跟踪（端到端设置下唯一模型）、评论生成（BLEU@1 31.3 vs. MatchVision 30.9）等下游任务上达到最优或竞争力水平（Table 4-6）。

## 整体框架

SoccerMaster 的核心设计动机源于一个关键瓶颈：现有足球视觉理解方法依赖孤立的、任务特定的专家模型，无法在单一框架内统一精细空间感知（如运动员检测、场地注册）与高级语义推理（如事件分类、评论生成）。为打破这一局限，SoccerMaster 通过**监督多任务预训练策略**，在共享的视觉编码器上同时学习空间细节（场地几何、运动员位置）和时间动态语义（事件、评论文本对齐），使得一个模型可以胜任从检测到描述的多种足球理解任务，且仅需轻量微调即可适配下游应用。

### 整体流程与模块关系

SoccerMaster 的整体 pipeline 由两大核心组件构成：**数据管线 SoccerFactory** 和 **模型架构 SoccerMaster**，二者协同工作形成完整的训练与推理闭环。

**SoccerFactory 自动化数据管线**（图2）负责从海量广播视频中生成大规模空间标注，为模型预训练提供必要监督。管线分三阶段运行：(i) **场地注册**——通过关键点与线段检测器建立图像与标准球场坐标之间的几何对应关系，并利用 PnL 模块估计相机参数；(ii) **跟踪与身份识别**——将帧级检测转化为运动员轨迹，包含检测、角色/队伍分类以及基于 ReID 的跟踪；(iii) **后处理精修**——借助 SAM2 分割和多数投票机制提升跟踪精度与时序一致性。SoccerFactory 在 SoccerNet-GSR 测试集上取得了 **GS-HOTA 64.1** 的成绩，超越挑战赛冠军 KIST-GSR（61.5），验证了其作为标注源的可靠性（Table 1）。

**SoccerMaster 模型架构**（图3）由视觉编码器和多个任务特定头组成。视觉编码器采用分阶段设计：前 $L_s$ 层保持标准空间自注意力，提取帧内空间特征 $\mathcal{F}_{\mathrm{spa}}$；后 $L_{st}$ 层引入交替的时空注意力（TimeSformer 式），通过时间注意力捕捉跨帧运动信息，生成富含时序语义的特征 $\mathcal{F}_{\mathrm{sem}}$。这种设计使得编码器能同时输出空间和语义两类表征，分别服务于下游的空间感知和语义推理任务。

在编码器之上，SoccerMaster 挂载了五个预训练任务头：
- **运动员检测与识别头 $\Psi_d$**：基于可变形 DETR 解码器，预测运动员边界框、角色（球员/裁判/守门员）和球衣号码。
- **场地关键点与线条检测头 $\Psi_k, \Psi_l$**：基于热图回归的场地点和线分割，为相机校准和位置投影提供几何基础。
- **事件分类头 $\Psi_e$**：两层 Transformer 编码器加分类器，识别 24 类足球事件。
- **视觉-语言对齐头 $\Psi_a$**：通过对比学习（SigLIP 损失）对齐视频语义特征与评论文本嵌入，实现跨模态检索。

总训练损失为各任务损失的加权组合：
$$
\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{a}} \mathcal{L}_{\mathrm{a}} + \lambda_{\mathrm{k}} \mathcal{L}_{\mathrm{k}} + \lambda_{\mathrm{l}} \mathcal{L}_{\mathrm{l}} + \lambda_{\mathrm{e}} \mathcal{L}_{\mathrm{e}} + \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}}
$$

### 输入输出流

**输入**：SoccerMaster 接受视频片段 $\mathcal{V}$（多帧图像序列）作为输入。对于空间感知任务（如检测、场地注册），使用逐帧处理；对于语义推理任务（如事件分类、视觉-语言对齐），利用时空注意力捕捉视频动态。

**预训练阶段**：编码器从视频中提取特征 $\mathcal{F} = \{\mathcal{F}_{\mathrm{spa}}, \mathcal{F}_{\mathrm{sem}}\}$，各任务头并行输出对应预测，联合优化多任务目标。预训练数据集总计约 **7.45M 帧**，其中约 2.75M 帧来自 SoccerFactory 自动生成的空间标注，4.71M 帧来自现有数据集的语义标注（Table 2）。

**下游适配**：预训练完成后，SoccerMaster 仅需简单微调即可迁移至下游任务。具体适配模块包括：用于评论生成的 **Q-Former**、用于相机校准的 **PnL 精修模块**、以及用于多目标跟踪的 **ID 解码器**。实验表明，这种轻量适配策略在相机校准（FS 86.8，超越 PnlCalib 的 78.6）、多目标跟踪和评论生成（BLEU@1 31.3）等任务上均达到最优或具有竞争力的结果（Table 4-6）。

### 关键设计决策

多任务预训练是 SoccerMaster 的核心创新点。消融实验（Table 12）揭示了一个重要的容量-性能权衡：在紧凑模型上，多任务训练使视觉-语言对齐 top-1 从 32.6% 提升至 36.8%，但运动员检测 AP@50 下降了 6.3 个百分点；而在全尺寸模型上，这一检测性能下降被消除，同时保持了语义任务的增益。这表明共享表征的学习效果与模型容量密切相关，全尺寸模型能更好地容纳多粒度知识的共存。

此外，SoccerFactory 自动标注数据的引入对空间感知任务贡献显著——在紧凑模型上，加入自动标注后运动员检测 AP@50 提升 4.3 点，mAP 提升 7.3 点（Table 7），证明了大规模自动标注在缓解空间监督稀缺方面的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/005_Figure_3.jpg]]
*Figure 3: SoccerMaster Architecture. (a) The architecture of SoccerMaster, which encodes both soccer videos and images through spatial and temporal attention modules to generate semantically rich representations. (b) The pretraining tasks and downstream adaptations of SoccerMaster across both spatial perception and semantic understanding tasks*

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/016_Figure_4.jpg]]
*Figure 4: Qualitative Results of SoccerFactory. Comparison between our predictions (left) and ground truth annotations (right) on the SoccerNet-GSR test set. Our pipeline demonstrates robust performance across diverse scenarios*

## 核心模块与公式推导

### 视觉编码器：空间与时空注意力的混合架构

SoccerMaster 的视觉编码器 $\Phi_{\mathrm{enc}}$ 是整个模型的表征核心，其设计目标是同时捕捉足球视频中的帧内空间细节和跨帧运动动态。编码器接收一个视频片段 $\mathcal{V} \in \mathbb{R}^{T \times H \times W \times 3}$，输出两类特征：

$$
\mathcal{F} = \{\mathcal{F}_{\mathrm{spa}}, \mathcal{F}_{\mathrm{sem}}\} = \Phi_{\mathrm{enc}}(\mathcal{V})
$$

其中 $\mathcal{F}_{\mathrm{spa}}$ 是空间特征，用于支持运动员检测、场地注册等精细空间感知任务；$\mathcal{F}_{\mathrm{sem}}$ 是语义特征，用于事件分类、视觉-语言对齐等高级语义推理任务。

编码器的核心创新在于**分阶段的注意力机制**。前 $L_s$ 层采用纯空间自注意力，每个 token 仅与同一帧内的其他 token 交互：

$$
\mathbf{z}_{t,i}^{(l+1)} = \mathrm{SpatialAttn}\left(\mathbf{z}_{t,i}^{(l)}, \{\mathbf{z}_{t,j}^{(l)}\}_{j=1}^{N}\right)
$$

这确保了模型首先建立对单帧空间结构的充分理解。后 $L_{st}$ 层引入交替的时空注意力（TimeSformer 式设计），每个时空块内先执行时间注意力，再执行空间注意力。时间注意力让同一空间位置上的 token 沿时间轴交互：

$$
\mathbf{z}_{t,i}^{(l+\frac{1}{2})} = \mathrm{TemporalAttn}\left(\mathbf{z}_{t,i}^{(l)}, \{\mathbf{z}_{t',i}^{(l)}\}_{t'=1}^{T}\right)
$$

紧随其后的空间注意力则在同一帧内聚合信息：

$$
\mathbf{z}_{t,i}^{(l+1)} = \mathrm{SpatialAttn}\left(\mathbf{z}_{t,i}^{(l+\frac{1}{2})}, \{\mathbf{z}_{t,j}^{(l+\frac{1}{2})}\}_{j=1}^{N}\right)
$$

这种设计将时序建模限定在深层，既降低了计算开销，又使浅层空间表征不受时序信息干扰，从而在空间感知和语义推理任务间取得平衡。

### 任务特定预测头

在共享编码器之上，SoccerMaster 部署了多个轻量任务头，统一输出所有预测结果：

$$
\{\mathcal{A}, \{\mathrm{id}_i\}, \mathcal{K}, \mathcal{L}, \mathbf{K}, \mathbf{R}, \mathbf{t}, \mathbf{e}, \hat{\mathcal{T}}\} = \Psi_{\mathrm{out}}(\mathcal{F})
$$

各预测头的具体设计如下：

- **运动员检测和识别头 $\Psi_d$**：基于可变形 DETR 解码器，从空间特征 $\mathcal{F}_{\mathrm{spa}}$ 中预测运动员边界框、角色（球员/裁判/守门员）和球衣号码。该头直接输出检测框集合 $\mathcal{A}$ 及对应的身份标签 $\{\mathrm{id}_i\}$。

- **场地关键点检测头 $\Psi_k$ 和线条检测头 $\Psi_l$**：采用基于热图的方法，分别预测场地关键点集合 $\mathcal{K}$ 和线段集合 $\mathcal{L}$。关键点定义为：

  $$
  \mathcal{K}_t = \{\mathbf{k}_i = (x_i, y_i; t_i) \mid i = 1, \ldots, N_k\} \in \mathbb{R}^{N_k \times 3}
  $$

  每个关键点包含图像坐标 $(x_i, y_i)$ 和类型 $t_i$。线段定义为：

  $$
  \mathcal{L}_t = \{\mathbf{l}_j = (\mathbf{p}_j^a, \mathbf{p}_j^b; t_j) \mid j = 1, \ldots, N_l\} \in \mathbb{R}^{N_l \times 5}
  $$

  每条线段由两个无序端点 $\mathbf{p}_j^a, \mathbf{p}_j^b$ 和线类型 $t_j$ 描述。检测到的关键点和线段随后通过 PnL 模块估计相机参数 $\mathbf{K}, \mathbf{R}, \mathbf{t}$，实现图像坐标到标准球场坐标的映射。

- **事件分类头 $\Psi_e$**：由两层 Transformer 编码器和分类器组成，从语义特征 $\mathcal{F}_{\mathrm{sem}}$ 中识别 24 类足球事件（如进球、角球、黄牌等），输出事件概率向量 $\mathbf{e}$。

- **视觉-语言对齐头 $\Psi_a$**：通过对比学习将视频语义特征与评论文本嵌入对齐，采用 SigLIP 损失函数，输出对齐后的文本表征 $\hat{\mathcal{T}}$。

### 多任务训练目标

SoccerMaster 的预训练采用多任务联合优化，总损失为各任务损失的加权和：

$$
\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{a}} \mathcal{L}_{\mathrm{a}} + \lambda_{\mathrm{k}} \mathcal{L}_{\mathrm{k}} + \lambda_{\mathrm{l}} \mathcal{L}_{\mathrm{l}} + \lambda_{\mathrm{e}} \mathcal{L}_{\mathrm{e}} + \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}}
$$

其中 $\mathcal{L}_{\mathrm{a}}$ 为运动员检测与识别损失，$\mathcal{L}_{\mathrm{k}}$ 和 $\mathcal{L}_{\mathrm{l}}$ 分别为关键点和线条检测损失，$\mathcal{L}_{\mathrm{e}}$ 为事件分类损失，$\mathcal{L}_{\mathrm{con}}$ 为视觉-语言对比损失。各损失权重 $\lambda$ 的具体配置见原文 Table 10。

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/013_Table_10.jpg]]
*Table 10: Loss Weights for Multi-task Training*

这一多任务目标的核心机理在于：空间感知任务（检测、场地注册）迫使编码器保留精细的几何与位置信息，而语义推理任务（事件分类、视觉-语言对齐）要求编码器提取高层时序动态和语义概念。两者在共享编码器中相互约束，使得学到的表征兼具空间精度和语义丰富性——这正是 SoccerMaster 能够以轻量微调适配多种下游任务的根本原因。

### 补充图表

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/002_Figure_2.jpg]]
*Figure 2: Automated Data Curation Pipeline. Our pipeline processes input videos through three stages: (i) field registration establishes geometric correspondences between image and canonical pitch coordinates via keypoint detection; (ii) tracking and identification transforms frames into athlete trajectories through detection, role and team classification, and ReID-based tracking; and (iii) post-processing refinement improves tracking accuracy through SAM2-based segmentation and ensures temporal consistency via majority voting*

## 实验与分析

SoccerMaster 的实验评估从三个层次展开：首先验证自动标注管线 SoccerFactory 的标注质量，随后在多任务预训练基准上对比通用视觉基础模型和足球专用模型，最后在多个下游任务上检验表征的迁移能力。所有关键数据均来自论文提供的 Table 1–Table 12 及附录。

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/003_Table_1.jpg]]
*Table 1: Comparison on GSR. SoccerMaster outperforms the challenge winner KIST-GSR on the SoccerNet-GSR test set. The best and second-best results are bolded and underlined*

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/015_Table_12.jpg]]
*Table 12: Ablation Study on the Impact of Multi-task Pretraining*

### 自动标注管线 SoccerFactory 的质量验证

SoccerFactory 本身是 SoccerMaster 数据闭环的核心组件，其输出质量直接决定空间感知预训练的上限。在 SoccerNet-GSR 游戏状态重建基准上，SoccerFactory 取得 **GS-HOTA 64.1**，超越该赛道冠军方案 KIST-GSR 的 61.5（Table 1）。该指标综合了检测精度 GS-DetA 51.5 和关联精度 GS-AssA 79.9，表明管线在运动员定位、角色识别和时序关联三个维度均达到领先水平。定性结果（Figure 4、Figure 5）进一步显示，SoccerFactory 在多种光照、视角和遮挡场景下均能稳定输出场地注册和跟踪结果，为后续预训练提供了可靠的空间监督信号。

### 预训练任务主结果

Table 3 是核心对比表，在冻结编码器、仅训练任务头的公平设置下，SoccerMaster 与通用视觉基础模型 **SigLIP 2**、**DINOv3** 以及足球专用模型 **MatchVision** 进行全面比较。关键发现如下：

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/006_Table_3.jpg]]
*Table 3: Performance Comparison on Pretraining Tasks. We compare SoccerMaster against both general-purpose VFMs (SigLIP2- L/16-512 [65] and DINOv3-L/16 [62]) and the soccer-specific MatchVision [57] using frozen encoders with trainable task-specific heads. “SoccerFactory Data” indicates training augmented with automatically generated data from our pipeline alongside existing datasets. Metrics include AP@50 and mAP for detection, jersey number (jn) and role classification accuracy, keypoint/line detection metrics, event classification accuracy, and video-commentary retrieval top-1 accuracy (computed within batches of 48)*

- **运动员检测**：SoccerMaster 的 AP@50 达到 **91.5**，相比 SigLIP 2 的 69.1 提升 **+22.4 点**，比 MatchVision 的 85.7 高出 5.8 点。mAP 指标同样大幅领先（68.7 vs. SigLIP 2 的 31.7），验证了空间感知预训练的有效性。
- **球衣号码与角色分类**：号码分类准确率 41.7%（MatchVision 31.8%），角色分类 93.2%（MatchVision 89.7%）。号码识别仍是瓶颈，后文将分析原因。
- **场地关键点与线条检测**：关键点 PCK@10 达 87.0，线条 mIoU 达 72.5，均显著优于 MatchVision（78.3 和 67.8）。
- **事件分类**：准确率 **77.2%**，比 MatchVision 的 65.3% 提升 **+11.9 点**，证明时空注意力模块有效捕获了视频动态语义。
- **视觉-语言对齐**：视频-评论检索 top-1 准确率从 MatchVision 的 4.0% 跃升至 **39.0%**（+35.0 点），这是 SoccerMaster 最显著的单项提升，说明多任务预训练使语义特征与自然语言建立了强对齐。

加入 SoccerFactory 自动生成的空间标注后（Table 3 中 “SoccerFactory Data” 行），所有空间感知指标进一步提升，运动员检测 AP@50 从 87.2 升至 91.5（+4.3 点），mAP 从 61.4 升至 68.7（+7.3 点），直接证明了自动标注管线对预训练的价值。

### 下游任务迁移能力

SoccerMaster 在下游任务上仅需轻量微调即可达到最优或竞争力水平：

- **相机校准**（Table 4）：在 SN22-test-center 上，微调后 Final Score 达 **86.8**，超过专用方法 PnlCalib 的 78.6（+8.2）。零样本推理（仅冻结编码器加可训练 PnL 模块）即达到 62.3，已具备一定泛化能力。
- **多目标跟踪**（Table 5）：SoccerMaster 是唯一采用端到端设置的模型，在 HOTA、MOTA、IDF1 等指标上与精心设计的跟踪流水线竞争，体现了统一表征对时序关联任务的支持。
- **评论生成**（Table 6）：在 MatchTime 基准上，BLEU@1 达 31.3，略超 MatchVision 的 30.9；ROUGE-L 和 METEOR 同样具有竞争力。值得注意的是，视觉-语言对齐预训练（top-1 39.0%）为评论生成提供了良好的初始化，但生成任务本身的增益相对温和，暗示从检索到生成的迁移仍需更精细的桥接设计。

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/008_Table_4.jpg]]
*Table 4: Comparison on Camera Calibration. Here*

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/007_Table_5.jpg]]
*Table 5: Comparison on Multiple Object Tracking. Notably, our model is the only one employing an end-to-end setting*

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/009_Table_6.jpg]]
*Table 6: Comparison on Commentary Generation*

### 消融实验与关键机制分析

**多任务预训练的影响**（Table 12，附录 D）。在紧凑模型变体上，多任务联合训练使视觉-语言对齐 top-1 从单任务训练的 32.6% 提升至 36.8%（+4.2 点），但运动员检测 AP@50 从 89.2 下降至 82.9（-6.3 点），暴露出任务间在有限容量下的竞争。全尺寸模型则可消除这一退化，检测性能保持稳定，说明模型容量是多任务收益的关键调节变量。

**自动标注数据的贡献**（Table 7）。单独消融 SoccerFactory 数据的影响：移除自动标注后，紧凑模型运动员检测 AP@50 下降 4.3 点，mAP 下降 7.3 点；全尺寸模型同样受益，但幅度略小。这确认了大规模空间标注对空间感知任务不可替代的作用。

**时空注意力的设计选择**。论文在 Section 5.2 中明确，前 $L_s$ 层保持纯空间自注意力以高效提取帧内特征，后 $L_{st}$ 层引入交替的时空注意力（TimeSformer 式）以捕获运动信息。这种“空间优先、时序增强”的设计避免了在全网络中引入高昂的时空注意力开销，同时保证了事件分类和视觉-语言对齐等语义任务所需的时序建模能力。事件分类 +11.9 点的提升是该设计有效性的直接证据。

### 失败模式与已知局限

论文坦诚列出了当前方法的不足，这些需要在解读实验结果时纳入考量：

1. **球衣号码识别**：准确率仅 41.7%，远低于其他任务。根本原因在于类别极度不平衡（null 类占绝大多数）和严重遮挡。当前方案缺乏对高分辨率局部区域的专门处理，单纯依赖全局特征难以区分细小数字。
2. **守门员分类**：易将守门员误判为普通球员。训练样本稀缺且队服颜色多变是表层原因，深层缺陷是模型缺乏关系推理能力——无法通过比较双方队服颜色来判断球员身份。
3. **球的检测与跟踪缺失**：当前空间感知任务未覆盖足球本身，限制了游戏状态重建的完整性。
4. **紧凑模型的容量瓶颈**：多任务预训练在紧凑模型上导致检测性能下降 6.3 点 AP@50，说明小模型难以同时容纳精细空间和高级语义知识，实际部署时需根据任务优先级选择模型规模或调整损失权重 $\lambda$（参见总损失公式 Eq. 14）。

### 重要图表结论速览

- **Table 2**：预训练数据总量约 745 万帧，其中空间感知任务 275 万帧，语义推理任务 471 万帧（1 FPS 采样），规模远超现有足球数据集。
- **Table 3**：SoccerMaster 在全部 8 项预训练指标上均超越 MatchVision，其中视觉-语言对齐提升最为显著（+35.0 点 top-1）。
- **Table 7**：自动标注数据对运动员检测的贡献为 +4.3 AP@50，是空间感知性能的关键驱动因素。
- **Table 12**：多任务预训练在紧凑模型上存在检测-对齐权衡，全尺寸模型可克服此问题。

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/004_Table_2.jpg]]
*Table 2: Pretraining Dataset Composition. Our pretraining dataset comprises approximately 7.45M frames across 248.3K video segments, with 2.75M frames for spatial perception tasks and 4.71M frames for semantic reasoning tasks (sampled at 1FPS)*

![[assets/figures/papers/paper_list_l2141_https_arxiv_org_abs_2512_11016/figures/010_Table_7.jpg]]
*Table 7: Ablation Study on the Impact of Automatically Generated Spatial Annotations*

## 方法谱系与知识库定位

### 从任务孤立到统一预训练：SoccerMaster 的方法谱系

SoccerMaster 的核心贡献在于打破现有足球视觉理解中“一任务一模型”的碎片化范式。在 SoccerMaster 之前，足球分析领域的方法论谱系大致可分为两条主线：

**1. 通用视觉基础模型（VFMs）的领域外迁移**

**SigLIP 2** 和 **DINOv3** 代表了通用视觉基础模型的两种主流路径——前者通过大规模视觉-语言对比学习获得语义丰富的表征，后者通过自监督学习捕获精细的空间结构。然而，如 Table 3 所示，当这些模型被冻结编码器并仅训练任务特定头时，它们在足球领域的表现存在明显短板：SigLIP 2 在运动员检测上仅达 69.1 AP@50，DINOv3 在视觉-语言对齐上的 top-1 准确率几乎为零。这一现象揭示了通用 VFMs 的根本局限——它们缺乏对足球场景中精细空间几何（如场地关键点、线条拓扑）和领域特定语义（如事件类型与评论文本的细粒度对应）的联合建模能力。

**2. 足球专用模型的单任务深耕**

以 **MatchVision** 为代表的足球专用模型通过领域特定的预训练和架构设计，在事件分类（65.3% 准确率）等语义任务上显著优于通用模型。但 MatchVision 的设计哲学仍然是“语义优先”——它在视觉-语言对齐上仅取得 4.0% top-1 准确率，且未在统一的框架内同时处理空间感知任务。这反映了现有足球专用模型的一个方法论瓶颈：语义理解与空间感知被割裂为独立的优化目标，模型无法从两者的协同中获益。

**SoccerMaster 的方法论突破**在于通过**监督多任务预训练**将上述两条主线融合：在单一视觉编码器上同时优化运动员检测与识别（空间感知）、场地关键点与线条检测（几何推理）、事件分类（时序语义）和视觉-语言对齐（跨模态语义）。这一策略的因果机制在于——共享的视觉编码器被迫同时学习“球在哪里”的细粒度空间特征和“发生了什么”的高层语义特征，从而形成多粒度的通用足球表征。Table 12 的消融实验提供了关键证据：多任务联合训练将视觉-语言对齐 top-1 从单任务训练的 32.6% 提升至 36.8%（+4.2 个百分点），验证了空间感知任务对语义表征的正向迁移效应。

### 与自动标注管线的协同演化

SoccerMaster 的方法论创新与 **SoccerFactory 自动标注管线**构成了一套协同演化的技术体系。传统足球分析模型主要依赖人工标注，空间标注成本极高，这从根本上限制了模型对场地几何的理解深度。SoccerFactory 通过三阶段管线（场地注册→跟踪与身份识别→后处理精修）实现了从广播视频到大规模空间标注的自动化，为 SoccerMaster 提供了约 2.7M 帧的空间监督数据。

这一数据-模型的协同关系在 Table 7 的消融实验中得到了量化验证：引入 SoccerFactory 自动生成的空间标注后，运动员检测 AP@50 提升 4.3 点，mAP 提升 7.3 点。这揭示了 SoccerMaster 方法论的一个关键边界条件——**精细空间感知能力的提升高度依赖于大规模空间标注的可用性**，而 SoccerFactory 正是突破这一数据瓶颈的使能技术。

### 适用边界与能力局限

尽管 SoccerMaster 在统一表征上取得了显著进展，其方法论仍存在明确的适用边界：

**1. 模型容量约束下的任务间权衡**

Table 12 和 Appendix D 的消融实验揭示了一个关键权衡：在紧凑模型变体上，多任务预训练虽然提升了视觉-语言对齐性能（+4.2 个百分点），却导致运动员检测 AP@50 下降 6.3 个百分点。这意味着在计算资源受限的场景下，空间感知与语义推理任务之间存在表征容量的竞争关系。全尺寸模型可以缓解这一冲突，但这一发现表明 SoccerMaster 的统一范式并非在所有模型规模下都能无代价地实现任务间的正向迁移。

**2. 空间感知范围的边界**

当前 SoccerMaster 的空间感知任务聚焦于运动员检测、场地关键点和线条检测，**未包含球的检测与跟踪**。这一设计选择意味着模型无法完整重建比赛的空间状态——球的轨迹是理解传球、射门等关键事件的核心空间线索。这一局限源于 SoccerFactory 自动标注管线当前的能力边界，也指向了方法论扩展的一个明确方向。

**3. 细粒度识别的瓶颈**

球衣号码识别受类别不平衡（null 类占主导）和遮挡影响，准确率有限；守门员分类易误判为普通球员，主要因为训练样本少且缺乏队服颜色的关系推理机制。这些失败模式表明，SoccerMaster 当前的纯视觉表征在处理需要高分辨率细节（球衣号码）和跨实例关系比较（守门员 vs. 同队球员的队服差异）的任务时仍有不足。

### 开放问题与未来方向

基于上述分析，SoccerMaster 的方法论体系面临以下开放问题：

1. **多模态信息的融合路径**：当前框架仅利用视觉和评论文本，如何融入音频评论、球员统计等模态以提升标注质量和模型对比赛上下文的理解，是一个自然的扩展方向。

2. **空间感知任务的完备性**：加入球的检测与跟踪将使得模型能够完整重建比赛的空间状态，但这也对 SoccerFactory 管线的自动标注能力提出了更高要求。

3. **效率与精度的架构权衡**：如何在统一的前向传播中兼顾高分辨率裁剪（球衣号码识别所需）与全局上下文（事件理解所需），同时保持计算效率，是一个有待解决的架构设计问题。

4. **关系推理的引入**：守门员分类的失败表明，纯前馈的视觉编码可能缺乏跨实例比较的能力。引入显式的关系推理模块（如比较队服颜色、空间位置关系）可能是一个有效的改进方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/SoccerMaster_A_Vision_Foundation_Model_for_Soccer_Understanding.pdf]]
