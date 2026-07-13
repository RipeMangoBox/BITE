---
title: Adapting a Pre-trained Single-Cell Foundation Model to Spatial Gene Expression Generation from Histology Images
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Adapting_a_Pre_trained_Single_Cell_Foundation_Model_to_Spatial_Gene_Expression_Generation_from_Histology_Images.pdf
project_link: null
code_link: "https://github.com/donghaifang/HINGE"
aliases:
- Adapting_a_Pre-t
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过身份初始化的SoftAdaLN层注入组织学和时间步条件到冻结的sc-FM，同时采用掩码扩散目标和对齐的预热课程，从而在保持预训练基因依赖模式的同时完成多模态条件生成。
primary_logic: 轻量级条件路径与身份初始化避免灾难性遗忘，掩码扩散与预热课程使训练目标与掩码自编码预训练对齐，从而在有限的空间转录组数据上成功迁移单细胞知识。
claims:
- HINGE通过添加身份初始化的SoftAdaLN模块，将预训练的sc-FM改造为组织学条件生成器，同时保留其大部分基因关系。
- SoftAdaLN的身份初始化确保在微调开始时保持原始行为，从而实现稳定的知识迁移。
- 掩码扩散过程的输入形式和监督模式均与掩码自编码预训练对齐，有效解决了目标失配问题。
- 预热课程通过初始阶段采样低掩码时间步，进一步稳定训练并与预训练体制匹配。
---

# Adapting a Pre-trained Single-Cell Foundation Model to Spatial Gene Expression Generation from Histology Images

> [!tip] 核心洞察
> 轻量级条件路径与身份初始化避免灾难性遗忘，掩码扩散与预热课程使训练目标与掩码自编码预训练对齐，从而在有限的空间转录组数据上成功迁移单细胞知识。

| 字段 | 内容 |
|------|------|
| 中文题名 | 将预训练的单细胞基础模型适配到从组织学图像生成空间基因表达 |
| 英文题名 | Adapting a Pre-trained Single-Cell Foundation Model to Spatial Gene Expression Generation from Histology Images |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.19766) · [Code](https://github.com/donghaifang/HINGE) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HINGE |
| Dataset | cSCC, Her2ST, Kidney |

> [!tip] 效果简介
> - cSCC 上，PCC-50 0.705 ± 0.006 vs 0.678 ± 0.013 (STFlow) (+0.027)。
> - Her2ST 上，PCC-50 0.566 ± 0.017 vs 0.543 ± 0.027 (STFlow) (+0.023)。
> - Kidney 上，PCC-50 0.428 ± 0.008 vs 0.391 ± 0.004 (STFlow) (+0.037)。

## 概要

空间转录组学（ST）能够在组织原位同时测量基因表达与组织形态，但其高昂的成本限制了大规模应用。从常规H&E染色组织学图像预测基因表达提供了一条经济可行的替代路径。现有方法大致分为两类：确定性回归方法（如**ST-Net**, He et al., Nature Biomedical Engineering 2020; **BLEEP**, Xie et al., NeurIPS 2023; **TRIPLEX**, Chung et al., CVPR 2024; **MERGE**, Ganguly et al., CVPR 2025）直接学习图像到表达的映射，以及基于扩散或流匹配的生成方法（如**Stem**, Zhu et al., ICLR 2025; **STFlow**, Huang et al., ICML 2025）建模表达分布。然而，这些方法均未显式利用基因间的依赖关系，导致预测的生物学一致性不足。

与此同时，单细胞基础模型（sc-FM）通过在大规模scRNA-seq数据上进行掩码自编码预训练，已经习得了丰富的基因间依赖模式。将这些知识迁移到组织学条件生成任务中，面临四个核心挑战：模态鸿沟（组织学图像与基因表达的异质性）、目标失配（掩码自编码与条件生成的任务差异）、细胞组成偏移（scRNA-seq与ST数据的分布差异）以及有限监督（ST数据稀缺）。

HINGE（HIstology-coNditioned GEneration）通过三项关键设计解决了上述挑战。**第一**，冻结预训练sc-FM的骨干网络，仅添加轻量级的身份初始化SoftAdaLN模块，在每个Transformer层注入组织学和时间步条件，从而在保持预训练基因关系的同时完成多模态条件生成。**第二**，引入掩码扩散过程替代传统高斯扩散，使前向过程的输入形式和监督模式均与掩码自编码预训练对齐，消解目标失配。**第三**，采用预热课程策略，在训练初期仅从低掩码区间采样时间步，进一步稳定训练并与预训练体制匹配。

在cSCC、Her2ST和Kidney三个数据集上，HINGE在PCC-50指标上分别达到0.705、0.566和0.428，一致优于包括STFlow在内的所有基线方法。消融研究证实，冻结预训练权重、掩码扩散目标以及身份初始化的SoftAdaLN调制是性能提升的关键因素。空间标记基因可视化和共表达相关性分析进一步表明，HINGE生成的表达谱在空间模式和基因间关系上均更接近真实数据。

**方法定位**：HINGE属于参数高效微调（parameter-efficient fine-tuning）范式，通过在冻结的预训练骨干上添加可学习的条件路径，将单细胞基础模型适配为组织学条件生成器。其核心创新在于将扩散生成过程重新表述为与掩码自编码预训练一致的形式，从而在有限ST数据上实现有效的知识迁移。

空间转录组学（Spatial Transcriptomics, ST）技术能够在组织切片的原始空间位置上同时测量数千个基因的表达，为理解组织微环境、细胞间通讯和疾病进展提供了前所未有的分辨率。然而，当前主流的基于测序的ST平台（如10x Visium）仍面临一个关键瓶颈：**基因表达测量与组织学图像采集通常在同一组织切片上交替进行，无法在同一物理切片上同时获得两种模态**。这意味着，对于仅保留H&E染色图像但缺乏配对表达数据的临床存档切片，研究者无法回溯其分子图谱。因此，**从组织学图像计算生成空间基因表达**成为一个具有重要临床和科研价值的前沿任务。

### 现有方法的缺口

近年来，研究者提出了多种从组织学图像预测基因表达的方法，大致可分为两类：

**确定性回归方法**直接学习从图像特征到表达值的映射。早期工作如**ST-Net**（He et al., Nature Biomedical Engineering, 2020）采用卷积网络进行逐点预测；**BLEEP**（Xie et al., NeurIPS 2023）引入双模态对比学习来对齐图像与表达嵌入；**TRIPLEX**（Chung et al., CVPR 2024）和**MERGE**（Ganguly et al., CVPR 2025）则分别通过多尺度特征融合和分层图神经网络进一步提升预测精度。然而，这些方法均将基因表达预测视为独立的逐基因回归问题，**完全忽略了基因之间复杂的共表达依赖关系**，导致预测结果的生物学一致性不足——例如，已知共调控基因的表达模式在预测中出现矛盾。

**条件生成方法**试图通过生成模型捕捉表达分布的多模态性。**Stem**（Zhu et al., ICLR 2025）采用条件扩散模型，**STFlow**（Huang et al., ICML 2025）则基于流匹配框架。尽管这些方法在表达分布的建模上优于回归方法，但它们从零开始学习基因间关系，受限于ST数据本身有限的样本量（通常每个数据集仅数十到数百个组织切片），难以充分学习高维基因空间中的复杂依赖结构。

### 核心机遇与挑战

与此同时，单细胞组学领域取得了突破性进展：大规模单细胞RNA测序（scRNA-seq）数据的积累催生了**单细胞基础模型（sc-FM）**的兴起。这些模型（如CellFM）在数千万个单细胞转录组上通过掩码自编码（Masked Autoencoding）进行预训练，在海量数据中习得了**高度结构化的基因间依赖关系**——这正是ST表达生成任务所急需的先验知识。

然而，将预训练的sc-FM直接迁移到组织学条件生成任务面临**四重挑战**：

1. **模态鸿沟**：sc-FM仅接受基因表达作为输入，缺乏处理组织学图像的条件注入机制。
2. **目标失配**：sc-FM的预训练目标是掩码自编码重构，而条件生成任务通常采用高斯扩散损失，两者在输入形式和监督模式上存在根本差异。
3. **细胞组成偏移**：scRNA-seq数据反映单细胞分辨率的表达，而ST数据每个测量点（spot）可能包含多个细胞的混合表达，分布特性显著不同。
4. **有限监督**：ST数据集规模远小于scRNA-seq预训练语料，直接微调极易导致灾难性遗忘，丧失预训练获得的基因关系知识。

### 本文动机

针对上述瓶颈，本文提出**HINGE（HIstology-coNditioned GEneration）**，核心思路是：**将预训练的sc-FM改造为组织学条件生成器，同时最大限度地保留其预训练习得的基因间依赖关系**。具体而言，HINGE通过在冻结的sc-FM骨干网络中插入轻量级的身份初始化条件调制模块，以最小的参数开销注入组织学和时间步信息；同时设计掩码扩散过程和预热训练课程，使生成任务的训练目标与掩码自编码预训练体制完全对齐。这一设计使得HINGE能够在仅数千个ST测量点的有限监督下，成功迁移来自数千万单细胞的基因关系知识，实现高生物学一致性的空间基因表达生成。

## 核心方法与创新机理

HINGE的核心创新并非提出全新的生成范式，而是通过**轻量级条件路径与预训练目标对齐**，将冻结的单细胞基础模型（sc-FM）成功迁移到组织学条件生成任务。其关键设计围绕一个因果关系展开：在有限的空间转录组（ST）数据上微调大规模预训练模型时，必须同时解决**模态鸿沟**（组织学图像→基因表达）、**目标失配**（掩码自编码→条件生成）和**灾难性遗忘**（覆盖预训练的基因依赖关系）三重挑战。

### 1. 身份初始化的SoftAdaLN条件注入

传统条件扩散模型通常从头训练或在预训练模型上直接添加交叉注意力层，但HINGE选择了一条更克制的路径：**冻结整个CellFM骨干网络，仅插入身份初始化的SoftAdaLN调制模块**。

具体而言，在每个Transformer子层中，HINGE插入一个轻量级的条件调制器，其核心运算为：

$$ \mathrm{SoftAdaLN}(\mathbf{h}_{\mathrm{in}} \mid \mathbf{c}_t) = \mathrm{SoftNorm}(\mathbf{h}_{\mathrm{in}}) \odot (\mathbf{1} + \mathbf{s}(\mathbf{c}_t)) + \kappa(\mathbf{c}_t) $$

其中条件嵌入 $\mathbf{c}_t$ 由组织学特征（UNI+CONCH双编码器）和扩散时间步联合编码得到，通过缩放向量 $\mathbf{s}$ 和偏移向量 $\kappa$ 对归一化后的特征进行自适应调制。关键创新在于**身份初始化**：训练开始时，$\mathbf{s} = \mathbf{0}$ 且 $\kappa = \mathbf{0}$，使得SoftAdaLN退化为恒等映射，确保模型初始行为与预训练状态完全一致。这种设计避免了随机初始化条件路径对预训练权重的破坏性干扰，使知识迁移过程平滑可控。

此外，HINGE引入了**可学习的软归一化**（SoftNorm）：

$$ \mathrm{SoftNorm}(\mathbf{h}_{\mathrm{in}}) = (1 - \eta) \mathbf{h}_{\mathrm{in}} + \eta \cdot \frac{\mathbf{h}_{\mathrm{in}} - \mu(\mathbf{h}_{\mathrm{in}})}{\sigma(\mathbf{h}_{\mathrm{in}}) + \varepsilon} $$

通过可学习参数 $\eta \in [0, 1]$ 在恒等映射与标准归一化之间平滑插值，为条件调制提供了更灵活的归一化基底。消融实验（Table 4）证实，移除SoftNorm或身份初始化均导致性能显著下降，验证了这两项设计对条件调制稳定性的关键作用。

### 2. 掩码扩散过程：弥合预训练与生成的目标鸿沟

这是HINGE最根本的方法论创新。CellFM通过**掩码自编码**（随机掩蔽部分基因并预测其原始值）在scRNA-seq数据上预训练，而标准扩散模型则对所有基因分量独立添加高斯噪声并预测完整去噪结果——两者在输入形式和监督模式上存在根本性失配。

HINGE引入的**随机掩码扩散过程**直接对齐了这两种范式。其前向过程定义为：

$$ q(\mathbf{X}_t, \mathbf{M}_t \mid \mathbf{X}_0, \mathbf{M}_0) = q(\mathbf{M}_t \mid \mathbf{M}_0) \delta_{\mathbf{M}_t \odot \mathbf{X}_0}(\mathbf{X}_t) $$

其中各基因的掩码状态服从独立的伯努利分布：

$$ q(\mathbf{M}_t \mid \mathbf{M}_0) = \prod_{g=1}^{G} \left[ \mathrm{Bern} \big( \mathbf{M}_t^{(g)} ; \bar{\alpha}_t \big) \right] $$

这里 $\bar{\alpha}_t$ 为累积可见性调度，控制不同时间步的掩码程度。训练目标则严格限制在**仅被掩蔽的基因分量**上：

$$ \mathcal{L}(\boldsymbol{\theta}) = \mathbb{E} \Big[ w_t \big\| \big( \mathbf{1} - \mathbf{m}_t \big) \odot \big( f_{\boldsymbol{\theta}} ( \mathbf{x}_t, t, \boldsymbol{\phi} ( \mathbf{c} ) ) - \mathbf{x}_0 \big) \big\|_2^2 \Big] $$

这一设计使HINGE的训练目标与CellFM的掩码自编码预训练在形式上完全一致：模型始终从部分可见的表达中预测被掩蔽部分。消融实验（Table 3）表明，掩码扩散显著优于标准高斯扩散，且移除掩码损失约束会导致性能大幅下降，证实了目标对齐是迁移成功的关键瓶颈。

### 3. 预热课程：稳定早期训练的调度策略

直接在全掩码范围内均匀采样时间步会导致训练初期模型面临过高的掩码率，与预训练阶段通常使用的较低掩码率形成冲突。HINGE的**预热课程**策略通过约束初始训练阶段的时间步采样范围来解决这一问题：在预热期间，仅从满足 $\bar{\alpha}_t \geq 1 - \rho$ 的低掩码区间采样时间步，使模型在可见基因占比较高的条件下逐步适应条件生成任务；预热结束后转为全区间均匀采样。

这一设计看似简单，但其作用机制深刻：它确保了微调初期的输入分布与预训练分布足够接近，使条件调制器能够在不破坏预训练表征的前提下逐步学习组织学映射。Table 3的消融显示，移除预热课程会导致训练不稳定和性能下降，尤其在小数据集上更为明显。

### 与基线方法的本质差异

相较于现有方法，HINGE的差异化创新体现在三个changed slots上：

- **条件注入机制**：不同于ST-Net、BLEEP等回归方法直接将组织学特征映射到表达空间，也不同于Stem、STFlow等生成模型从头学习条件依赖，HINGE通过身份初始化的SoftAdaLN在冻结的预训练骨干上注入条件，实现了对预训练基因关系的最大程度保留。
- **扩散过程**：不同于Stem的高斯扩散和STFlow的流匹配，HINGE的掩码扩散在扩散范式层面就与预训练目标对齐，而非仅在损失函数层面修补。
- **训练课程**：预热课程是HINGE独有的训练策略，现有方法均未考虑预训练与微调阶段的分布偏移问题。

**证据强度评估**：上述三项创新的有效性均通过消融实验获得直接验证（Table 2-4），证据链完整且置信度高。但需注意，目前仅在CellFM这一单一sc-FM上进行了验证，该方法在其他预训练模型（如scGPT、scFoundation）上的泛化性尚需进一步实验确认。

HINGE 的整体设计遵循“冻结预训练知识 + 轻量条件注入”的适配范式，将大规模单细胞 RNA-seq 上预训练的掩码自编码基础模型 **CellFM** 改造为组织学图像条件下的空间基因表达生成器。图 1 给出了框架概览：图 1(a) 展示 CellFM 的原始架构，图 1(b) 则呈现 HINGE 如何在该骨干网络上叠加条件通路。

### 输入输出流

系统的输入包括两个模态：

- **组织学图像**：来自空间转录组切片的 H&E 染色图像补丁，通过双编码器框架 **UNI** 和 **CONCH** 分别提取视觉特征，二者拼接后送入条件嵌入网络。
- **目标基因表达**：训练时提供完整的基因表达谱 $\mathbf{X}_0 \in \mathbb{R}^G$（$G$ 为基因数，受限于 CellFM 的预训练词汇表 24,078 个基因）；推理时从完全掩码状态出发，通过迭代去掩码逐步生成。

输出为每个空间位点（spot）的预测基因表达谱，可直接用于下游分析。

### 模块关系

HINGE 的 pipeline 由以下核心模块串联构成：

1. **组织学编码器**：采用 UNI + CONCH 双编码器，从 H&E 图像补丁中提取互补的视觉特征。消融实验（Table 5）证实该组合在多种组织学特征提取器中表现最优。

2. **条件嵌入网络**：将拼接后的组织学特征与扩散时间步 $t$ 共同编码为全局条件嵌入 $\mathbf{c}_t$，作为后续所有 Transformer 层的共享调制信号。

3. **SoftAdaLN 调制模块**：在 CellFM 的每一层 Transformer 中插入身份初始化的 SoftAdaLN。该模块以残差门控方式将 $\mathbf{c}_t$ 注入冻结的骨干网络，实现组织学条件与时间步条件的层级调制。具体地，每个子层依次经过：
   - **SoftNorm**：通过可学习参数 $\eta$ 在恒等映射与标准归一化之间平滑插值，公式为 $\mathrm{SoftNorm}(\mathbf{h}_{\mathrm{in}}) = (1 - \eta) \mathbf{h}_{\mathrm{in}} + \eta \cdot \frac{\mathbf{h}_{\mathrm{in}} - \mu(\mathbf{h}_{\mathrm{in}})}{\sigma(\mathbf{h}_{\mathrm{in}}) + \varepsilon}$；
   - **SoftAdaLN 调制**：利用条件嵌入产生的缩放 $\mathbf{s}$ 和偏移 $\kappa$ 对特征进行自适应变换，$\mathrm{SoftAdaLN}(\mathbf{h}_{\mathrm{in}} \mid \mathbf{c}_t) = \mathrm{SoftNorm}(\mathbf{h}_{\mathrm{in}}) \odot (\mathbf{1} + \mathbf{s}(\mathbf{c}_t)) + \kappa(\mathbf{c}_t)$；
   - **门控残差连接**：通过条件门控 $\tau(\mathbf{c}_t)$ 控制变换特征的保留度，并与残差路径融合后经冻结的 LayerNorm 输出。

   身份初始化确保微调开始时调制模块输出恒等于原始 CellFM 行为，从而避免灾难性遗忘。消融实验（Table 4）表明，移除 SoftNorm 或身份初始化均会导致性能下降，验证了二者对条件调制稳定性的关键作用。

4. **冻结的 CellFM 骨干网络**：提供从大规模 scRNA-seq 掩码自编码预训练中习得的基因间依赖关系，参数完全冻结。消融实验（Table 2）证实冻结预训练权重并仅微调条件调制器显著优于完全微调或完全冻结，印证了在有限 ST 数据上保留 sc-FM 先验知识的重要性。

5. **掩码扩散采样器**：前向过程对各基因分量独立施加伯努利掩码，$q(\mathbf{M}_t \mid \mathbf{M}_0) = \prod_{g=1}^{G} [\mathrm{Bern}(\mathbf{M}_t^{(g)}; \bar{\alpha}_t)]$，表达由当前掩码决定：$q(\mathbf{X}_t, \mathbf{M}_t \mid \mathbf{X}_0, \mathbf{M}_0) = q(\mathbf{M}_t \mid \mathbf{M}_0) \delta_{\mathbf{M}_t \odot \mathbf{X}_0}(\mathbf{X}_t)$。逆过程从完全掩码状态出发，迭代预测被掩码基因并填充去噪值，最终生成完整表达谱。

### 训练策略

训练目标仅在当前被掩蔽的基因分量上计算加权 MSE 损失：
$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E} \Big[ w_t \big\| (\mathbf{1} - \mathbf{m}_t) \odot \big( f_{\boldsymbol{\theta}} (\mathbf{x}_t, t, \boldsymbol{\phi} (\mathbf{c})) - \mathbf{x}_0 \big) \big\|_2^2 \Big]$$
这使得输入形式与监督模式均与 CellFM 的掩码自编码预训练对齐，有效解决了目标失配问题。

此外，HINGE 采用**预热课程**策略：初始训练阶段仅从低掩码区间（$\bar{\alpha}_t \geq 1 - \rho$）采样时间步，随后转为全区间均匀采样。消融实验（Table 3）表明，掩码扩散配合预热课程优于高斯扩散及无预热课程的掩码扩散变体，证实目标对齐与课程学习有效弥合了预训练与生成任务间的鸿沟。

![[assets/figures/papers/paper_list_l2436_https_arxiv_org_abs_2603_19766/figures/001_Figure_1.jpg]]
*Figure 1: Overview of HINGE. (a) Depicts the CellFM architecture, which is a single-cell foundation model (sc-FM) pre-trained on scRNA-seq with masked autoencoding. (b) In HINGE, the conditional denoising model is instantiated from CellFM and augmented with identity-initialized SoftAdaLN that injects histology and timestep context into each transformer layer within a stochastic masked diffusion process. This design keeps the training objective aligned with CellFM’s masked autoencoding for coherence in ST, thereby largely preserving the gene relationships learned from scRNA-seq*

HINGE 在冻结的 CellFM 骨干网络上叠加轻量级条件路径，将预训练的单细胞基础模型改造为组织学条件生成器。其核心由三个紧密协作的模块构成：掩码扩散过程、冻结的 Transformer 骨干，以及身份初始化的 SoftAdaLN 条件注入机制。

**掩码扩散过程**是弥合预训练与生成任务之间目标鸿沟的关键。前向过程对基因表达分量执行随机掩码，而非传统的高斯噪声注入。给定初始干净表达 $\mathbf{X}_0$ 和全可见掩码 $\mathbf{M}_0 = \mathbf{1}$，在时刻 $t$ 的联合分布定义为：

$$q(\mathbf{X}_t, \mathbf{M}_t \mid \mathbf{X}_0, \mathbf{M}_0) = q(\mathbf{M}_t \mid \mathbf{M}_0) \delta_{\mathbf{M}_t \odot \mathbf{X}_0}(\mathbf{X}_t)$$

其中 $\delta$ 为狄拉克函数，确保 $\mathbf{X}_t$ 完全由当前掩码 $\mathbf{M}_t$ 和原始表达 $\mathbf{X}_0$ 的逐元素乘积决定。各基因分量的掩码状态服从独立的伯努利分布：

$$q(\mathbf{M}_t \mid \mathbf{M}_0) = \prod_{g=1}^{G} \left[ \mathrm{Bern} \big( \mathbf{M}_t^{(g)} ; \bar{\alpha}_t \big) \right]$$

$\bar{\alpha}_t$ 为累积可见性调度参数，控制时刻 $t$ 每个基因被保留（可见）的概率。$\bar{\alpha}_t$ 从 $1$（完全可见）单调递减至 $0$（完全掩码），形成逐步揭示基因信息的扩散过程。这一设计使输入形式与 CellFM 预训练时的掩码自编码体制完全一致。

**训练目标**仅在被掩码的基因分量上计算加权均方误差。设 $f_{\boldsymbol{\theta}}$ 为去噪网络，$\boldsymbol{\phi}(\mathbf{c})$ 为组织学特征提取器输出的图像条件，$\mathbf{m}_t$ 为时刻 $t$ 的掩码指示向量，损失函数为：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E} \Big[ w_t \big\| \big( \mathbf{1} - \mathbf{m}_t \big) \odot \big( f_{\boldsymbol{\theta}} ( \mathbf{x}_t, t, \boldsymbol{\phi} ( \mathbf{c} ) ) - \mathbf{x}_0 \big) \big\|_2^2 \Big]$$

$w_t$ 为时间步相关的权重系数，$( \mathbf{1} - \mathbf{m}_t )$ 确保梯度仅通过当前被掩蔽的基因回传。这种选择性监督模式与 CellFM 预训练时的掩码自编码损失完全对齐，从根本上解决了目标失配问题。

**SoftAdaLN 条件注入**是 HINGE 实现多模态融合的核心机制。每个 Transformer 层内插入一个身份初始化的调制模块，包含三个关键操作。首先是可学习的软归一化 SoftNorm：

$$\mathrm{SoftNorm}(\mathbf{h}_{\mathrm{in}}) = (1 - \eta) \mathbf{h}_{\mathrm{in}} + \eta \cdot \frac{\mathbf{h}_{\mathrm{in}} - \mu(\mathbf{h}_{\mathrm{in}})}{\sigma(\mathbf{h}_{\mathrm{in}}) + \varepsilon}$$

其中 $\eta \in [0, 1]$ 为可学习参数，在恒等映射（$\eta=0$）与标准归一化（$\eta=1$）之间平滑插值。随后，由组织学特征和扩散时间步联合编码得到的全局条件嵌入 $\mathbf{c}_t$ 生成缩放因子 $\mathbf{s}(\mathbf{c}_t)$ 和偏移量 $\kappa(\mathbf{c}_t)$，对 SoftNorm 输出进行自适应调制：

$$\mathrm{SoftAdaLN}(\mathbf{h}_{\mathrm{in}} \mid \mathbf{c}_t) = \mathrm{SoftNorm}(\mathbf{h}_{\mathrm{in}}) \odot (\mathbf{1} + \mathbf{s}(\mathbf{c}_t)) + \kappa(\mathbf{c}_t)$$

身份初始化的关键在于：训练开始时 $\mathbf{s}(\mathbf{c}_t)$ 和 $\kappa(\mathbf{c}_t)$ 均初始化为零向量，SoftNorm 的 $\eta$ 初始化为 $0$，使得整个调制模块退化为恒等映射，完全保留预训练模型在无图像条件下的原始行为。最后，调制后的特征通过条件门控残差连接与原始输入融合：

$$\mathbf{h}_{\mathrm{out}} = \mathrm{LN}\big(\tau(\mathbf{c}_t) \odot \mathbf{u} + \lambda \mathbf{h}_{\mathrm{in}}\big)$$

其中 $\mathbf{u}$ 为经 SoftAdaLN 调制后的特征，$\tau(\mathbf{c}_t)$ 为条件门控系数，$\lambda$ 为残差权重，$\mathrm{LN}$ 为冻结的 LayerNorm 层。这种轻量级的条件注入设计确保仅新增约 1% 的可训练参数，同时有效避免灾难性遗忘。

**预热课程**进一步稳定早期训练。在初始阶段，扩散时间步 $t$ 仅从低掩码区间采样（即 $\bar{\alpha}_t \geq 1 - \rho$），使模型先学习在少量基因被掩码的条件下进行预测，与预训练时的低掩码率场景相匹配。完成预热后，$t$ 转为全区间均匀采样，逐步过渡到完整的生成任务。

## 实验与关键发现

### 主实验结果

HINGE在三个空间转录组数据集（cSCC、Her2ST、Kidney）上系统评估了从组织学图像预测基因表达的性能，与六种代表性基线方法进行对比：确定性回归方法**ST-Net**（He et al., Nature Biomedical Engineering, 2020）、**BLEEP**（Xie et al., NeurIPS 2023）、**TRIPLEX**（Chung et al., CVPR 2024）、**MERGE**（Ganguly et al., CVPR 2025），以及生成式方法**Stem**（Zhu et al., ICLR 2025）和**STFlow**（Huang et al., ICML 2025）。所有方法在相同的数据集划分和三个随机种子上评估，报告均值与标准差。

如Table 1所示，HINGE在所有数据集和指标上均取得最优或次优结果。以核心指标PCC-50（前50个高变基因的平均Pearson相关系数）为例：在cSCC数据集上，HINGE达到0.705±0.006，相比最强基线STFlow（0.678±0.013）提升2.7个百分点；在Her2ST上达到0.566±0.017，超越STFlow（0.543±0.027）2.3个百分点；在Kidney上达到0.428±0.008，较STFlow（0.391±0.004）提升3.7个百分点。在PCC-200、MSE和MAE指标上，HINGE同样保持一致的领先趋势，表明其在不同组织类型和数据规模下具有稳健的预测能力。

为评估切片级性能差异的统计显著性，Figure 2展示了各数据集上逐切片的PCC-50和PCC-200箱线图，并采用配对Wilcoxon符号秩检验进行两两比较。结果显示，HINGE在多数切片上显著优于各基线方法（*p<0.05，**p<0.01，***p<0.001），尤其在Kidney数据集的PCC-200上，HINGE相对于所有基线的优势均达到极显著水平。

Table S.1汇总了三个数据集的统计信息，包括患者数量、每切片spot数和基因数范围以及平台类型，为上述跨数据集比较提供了必要的背景。

### 消融实验

为验证HINGE各设计选择的有效性，作者进行了系统的消融研究。

**sc-FM适应方案**。Table 2比较了四种预训练权重利用策略：（1）完全冻结CellFM（无微调）；（2）完全微调所有参数；（3）冻结骨干但添加可训练的适配器模块；（4）HINGE的冻结骨干+SoftAdaLN方案。结果表明，完全微调在有限ST数据上表现最差，验证了保留预训练基因关系的重要性；完全冻结缺乏条件适应能力；而HINGE方案在PCC-50和PCC-200上均取得最佳结果，证实冻结骨干并仅微调轻量级条件调制器是平衡知识保留与任务适应的有效策略。

**扩散过程与训练目标**。Table 3对比了高斯扩散、掩码扩散变体及完整HINGE目标。将HINGE的掩码扩散替换为标准高斯扩散后，性能显著下降，说明掩码扩散过程与预训练掩码自编码目标的对齐至关重要。移除预热课程（warm-start curriculum）同样导致性能退化，表明初始阶段采样低掩码时间步有助于稳定训练并与预训练体制匹配。此外，仅在掩码基因上计算损失（而非全基因损失）进一步提升了预测精度，验证了监督模式对齐的必要性。

**条件注入机制**。Table 4比较了不同的条件调制方案。完整SoftAdaLN优于移除SoftNorm（仅使用标准LayerNorm）的变体，也优于移除身份初始化的变体，表明可学习的软归一化和身份初始化对条件调制的稳定性均不可或缺。身份初始化确保微调开始时模型保持原始行为，避免灾难性遗忘。

**组织学编码器**。Table 5评估了不同视觉编码器的影响。UNI+CONCH双编码器组合在所有编码器配置中取得最佳性能，验证了融合多尺度组织学特征对下游生成任务的有效性。

补充材料中的Table S.2和Table S.3分别在Her2ST和Kidney数据集上复现了上述消融结论，进一步增强了结论的可靠性。Table S.4探索了不同掩码调度方案的影响，Table S.5报告了各方法的推理效率，其中HINGE在保持高性能的同时内存开销可控。

### 定性分析

Figure 3展示了cSCC切片上KRT6A基因和Her2ST切片上GNAS基因的空间表达可视化。HINGE预测的空间表达模式与真实值高度一致，能够准确捕捉组织区域特异的表达热点，而基线方法（如ST-Net、BLEEP、Stem）在空间细节上存在不同程度的模糊或偏差。

Figure 4进一步从基因间共表达角度评估生物学一致性。在Kidney切片的HMHVG基因集上，HINGE预测的基因-基因相关矩阵与真实值最为接近，表明其成功保留了预训练sc-FM中习得的基因依赖关系，而其他方法在共表达结构上出现明显失真。这一结果直接验证了HINGE的核心设计动机——通过冻结骨干和掩码扩散对齐，将单细胞基础模型中的基因关系知识有效迁移至空间转录组生成任务。

### 失败模式与局限性

尽管HINGE在定量和定性评估中均表现优异，仍存在若干局限。首先，目前仅基于单一的单细胞基础模型CellFM进行验证，对其他sc-FM（如scGPT、scFoundation）的泛化性尚不明确。其次，基因列表受限于CellFM的预训练词汇表（24,078个基因），可能遗漏某些数据集的特有基因，影响特定生物学问题的分析。第三，HINGE未显式利用空间位置信息，仅在表达空间建模，可能丢失空间上下文依赖，这在高分辨率空间转录组数据中尤为突出。最后，训练与推理仍依赖GPU，在部分高分辨率切片上内存开销较大（见Table S.5），限制了其在大规模临床部署中的实用性。这些局限性指向了未来工作的方向，包括多sc-FM适配、空间位置编码注入、以及模型轻量化等。

![[assets/figures/papers/paper_list_l2436_https_arxiv_org_abs_2603_19766/figures/002_Table_1.jpg]]
*Table 1: Comparison on cSCC, Her2ST, and Kidney datasets using PCC-50, PCC-200, MSE, and MAE. Scores are averaged over test slices and three random seeds, reported as mean ± standard deviation. Best results are in bold, and second-best are underlined*

![[assets/figures/papers/paper_list_l2436_https_arxiv_org_abs_2603_19766/figures/009_Table_3.jpg]]
*Table 3: Comparison of Gaussian diffusion, masked diffusion variants, and the full HINGE objective*

![[assets/figures/papers/paper_list_l2436_https_arxiv_org_abs_2603_19766/figures/006_Table_4.jpg]]
*Table 4: Comparison of alternative conditioning mechanisms*

![[assets/figures/papers/paper_list_l2436_https_arxiv_org_abs_2603_19766/figures/011_Table_S.2.jpg]]
*Table S.2: Ablations on Her2ST. Component-wise analysis of HINGE variants on the Her2ST (A1) dataset*

![[assets/figures/papers/paper_list_l2436_https_arxiv_org_abs_2603_19766/figures/012_Table_S.3.jpg]]
*Table S.3: Ablations on Kidney. Component-wise analysis of HINGE variants on the Kidney (IU-F52) dataset*

## 定位与知识库关联

### 基线方法与差异化定位

HINGE 处于**组织学图像到空间基因表达生成**这一任务线上，其基线方法可划分为两类范式：确定性回归与生成式建模。

**确定性回归方法**直接从组织学图像映射到表达谱，不显式建模基因间依赖关系。代表工作包括 **ST-Net**（He et al., *Nature Biomedical Engineering*, 2020），首次以端到端方式从H&E染色图像预测空间基因表达；**BLEEP**（Xie et al., NeurIPS 2023）引入双模态对比学习，将图像与表达嵌入到共享空间进行匹配；**TRIPLEX**（Chung et al., CVPR 2024）通过多尺度特征融合提升回归精度；**MERGE**（Ganguly et al., CVPR 2025）则采用分层图神经网络捕获组织区域间的空间依赖。这些方法的共同瓶颈在于：输出层为逐基因独立预测，未显式建模基因间的共表达与调控关系，导致预测的生物学一致性不足。

**生成式建模方法**试图通过概率生成框架弥补上述缺陷。**Stem**（Zhu et al., ICLR 2025）首次将条件扩散模型引入该任务，对表达谱各基因分量独立施加高斯噪声并逐步去噪；**STFlow**（Huang et al., ICML 2025）采用流匹配框架，以更高效的训练方式实现类似目标。然而，这两类生成方法均从零开始训练，未能利用大规模单细胞数据中蕴含的基因间依赖先验。

HINGE 的核心差异化在于**将预训练的单细胞基础模型（sc-FM）作为知识锚点**，而非从随机初始化出发。这一选择带来了根本性的方法学挑战：sc-FM（此处为 CellFM）在数百万单细胞转录组上以掩码自编码目标预训练，其输入输出空间和训练体制与组织学条件生成存在三重鸿沟——**模态鸿沟**（sc-FM仅接受表达输入，无图像通道）、**目标失配**（掩码自编码 vs. 扩散去噪）、以及**数据分布偏移**（scRNA-seq vs. 空间转录组）。HINGE 通过三个协同设计弥合这些鸿沟：

1. **身份初始化的SoftAdaLN条件路径**：在冻结的CellFM各Transformer层插入轻量级调制模块，以组织学特征和扩散时间步生成缩放与偏移参数。身份初始化确保微调起始时模型行为与原sc-FM完全一致，避免灾难性遗忘。这与LoRA等低秩适配方法形成对比——后者通常用于语言模型，而HINGE的SoftAdaLN专为连续表达空间的条件注入设计，且包含可学习的软归一化插值机制。

2. **掩码扩散过程**：摒弃高斯扩散对各基因分量独立加噪的方式，转而采用随机掩码扩散——逐步掩蔽基因分量，仅要求模型预测被掩蔽部分。这一设计的输入形式（部分可见的表达谱）和监督模式（仅在被掩蔽基因上计算损失）与sc-FM的掩码自编码预训练完全对齐，从根源上解决了目标失配问题。

3. **预热课程**：初始训练阶段仅在低掩码区间采样时间步，使模型先学会在少量掩码下利用组织学信息进行简单补全，再逐步过渡到高掩码的困难场景。这一课程策略进一步平滑了从预训练到生成任务的过渡。

### 适用边界

HINGE 的当前设计存在以下适用边界：

- **sc-FM依赖性**：方法目前仅在 **CellFM** 上验证，该模型预训练基因词汇表为24,078个基因。对于超出该词汇表的基因，HINGE无法进行预测。此外，不同sc-FM（如scGPT、scFoundation、Geneformer）的架构和预训练策略差异可能影响适配效果，泛化性尚需进一步验证。

- **空间上下文缺失**：HINGE仅利用组织学图像补丁的视觉特征作为条件，未显式注入空间坐标或邻域关系。对于高度依赖空间位置信息的基因表达模式（如发育梯度、肿瘤微环境边界），该方法可能丢失关键的空间上下文。

- **计算资源需求**：尽管CellFM骨干被冻结，条件编码器（UNI + CONCH双编码器）和SoftAdaLN模块仍需GPU进行训练与推理。在高分辨率组织切片上，组织学特征提取和扩散采样过程的内存开销较大。

### 局限与开放问题

**已识别的局限**：

1. **单sc-FM验证**：当前实验仅基于CellFM，未探索其他预训练单细胞模型的适配效果。不同sc-FM在基因覆盖度、嵌入空间结构和预训练数据分布上的差异，可能导致HINGE框架的迁移效果显著不同。

2. **基因词汇表受限**：受限于CellFM的预训练基因集，某些空间转录组数据集中具有重要生物学意义的基因可能被遗漏，限制了方法在特定研究场景中的适用性。

3. **空间信息利用不足**：方法在表达空间独立建模每个spot，未利用空间邻域关系或组织拓扑结构，可能影响空间表达模式的一致性和平滑性。

**开放问题**：

- **跨sc-FM泛化性**：该方法在scGPT、scFoundation等其他预训练sc-FM上的表现如何？是否需要针对不同sc-FM的架构特点调整条件注入策略？

- **空间坐标注入**：是否可以通过在条件嵌入中融合空间位置编码或图神经网络聚合的邻域特征，进一步提升预测的空间一致性？

- **多模态扩展**：该框架能否扩展至蛋白质丰度、染色质可及性等其他空间多模态数据的生成？掩码扩散与身份初始化适配策略是否具有跨模态通用性？

- **推理效率优化**：如何通过模型蒸馏、量化或减少扩散采样步数来降低推理延迟，以适应大规模临床样本的快速处理需求？

## 原文 PDF

![[paperPDFs/CVPR_2026/Adapting_a_Pre_trained_Single_Cell_Foundation_Model_to_Spatial_Gene_Expression_Generation_from_Histology_Images.pdf]]
