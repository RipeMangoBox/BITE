---
title: "MaxSim: Fine-grained Motion Retrieval via Joint-Angle Motion Images and Token-Patch Late Interaction"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/MaxSim_Fine_grained_Motion_Retrieval_via_Joint_Angle_Motion_Images_and_Token_Patch_Late_Interaction.pdf
project_link: null
code_link: null
aliases:
- MJAMIMLIM
- MaxSim
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 提出基于关节角度的运动表示（将局部关节运动独立映射到伪图像的特定区域）和 MaxSim token-patch 延迟交互机制（显式地对齐文本词元和运动区块），并辅以掩码语言建模（MLM）正则化增强文本词元的上下文信息。
primary_logic: 通过关节角度解耦局部与全局运动，使 ViT 的每个 patch 自然对应特定关节；MaxSim 允许每个文本词元动态匹配最相关的运动区块，从而保留并利用局部运动细节，实现更精确、可解释的跨模态对齐。
claims:
- 采用关节角度表示并与 MaxSim 结合时，在 HumanML3D 上 T2M R@5 比基于位置的表示提升 +2.85%
- 在基于位置的表示上添加 MLM 正则化，使 HumanML3D 上的 T2M R@1 从 10.88% 提升至 11.86%，M2T R@1 从 11.82% 提升至 12.93%
- 定性结果显示，交互热力图的激活区域集中于与查询语义直接对应的身体关节和时间段，例如“右腿高踢”时右髋、膝、踝区域的激活
- HumanML3D 上 T2M R@10 = 43.80
---

# MaxSim: Fine-grained Motion Retrieval via Joint-Angle Motion Images and Token-Patch Late Interaction

> [!tip] 核心洞察
> 通过关节角度解耦局部与全局运动，使 ViT 的每个 patch 自然对应特定关节；MaxSim 允许每个文本词元动态匹配最相关的运动区块，从而保留并利用局部运动细节，实现更精确、可解释的跨模态对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | MaxSim：基于关节角度运动图像与Token-Patch延迟交互的细粒度运动检索 |
| 英文题名 | MaxSim: Fine-grained Motion Retrieval via Joint-Angle Motion Images and Token-Patch Late Interaction |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/pdf/2603.09930v1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MaxSim (Joint-Angle Motion Image + MaxSim Late Interaction + MLM) |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，T2M R@10 43.80 vs 40.78 (MoPatch global) (+3.02)；M2T R@10 41.45 vs 38.73 (MoPatch global) (+2.72)。

## 概要

文本-运动检索旨在根据自然语言描述从大规模运动数据库中匹配最相关的运动序列。现有方法普遍采用**双编码器架构**，将运动序列和文本描述分别压缩为单一的全局嵌入向量，通过余弦相似度进行匹配。这种全局池化策略不可避免地丢失了细粒度的局部对应信息——例如“右手画圈同时左脚前踏”这样的复合描述中，不同身体部位与时间段的运动细节在全局向量中被混叠，导致检索精度受限且缺乏可解释性。

针对上述瓶颈，本文提出 **MaxSim**，核心思路包含两个层面：**（1）关节角度运动表示**——通过逆运动学将骨架运动解耦为局部关节角度特征，并将其构造为结构化的伪图像（Motion Image），使 ViT 的每个 patch 天然对应特定关节；**（2）MaxSim token-patch 延迟交互**——保留文本词元和运动区块的完整嵌入序列，允许每个文本词元动态匹配最相关的运动区块，并通过平均各词元的最大相似度得到最终的跨模态匹配分数。此外，引入**掩码语言建模（MLM）正则化**增强文本词元的上下文信息。这一设计使得检索过程不仅更精确，还具备天然的可解释性——交互热力图可直接显示查询词元与身体关节的对应关系。

在 HumanML3D 和 KIT-ML 两个标准基准上，MaxSim 在文本到运动（T2M）和运动到文本（M2T）两个方向的检索任务中均超越了现有最优方法。消融实验证实，关节角度表示与 MaxSim 延迟交互的结合是性能提升的关键驱动因素，而 MLM 正则化在 M2T 方向带来尤为显著的增益。

### 问题背景：文本-运动检索的挑战

文本-运动检索（Text-to-Motion Retrieval）旨在根据自然语言描述从大规模运动数据库中检索最匹配的3D人体运动序列。该任务在动画制作、游戏开发和人机交互等领域具有重要应用价值。然而，该任务面临的核心挑战在于**跨模态语义对齐**——自然语言的离散符号系统与人体运动的连续时空信号之间存在巨大的语义鸿沟。

现有主流方法普遍采用**双编码器架构**（dual-encoder framework），如 **TMR**（Petrovich et al., ICCV 2023）等，将运动序列和文本描述分别编码为单一的全局嵌入向量，再通过余弦相似度进行匹配。这种全局池化策略虽然简洁高效，却不可避免地**丢弃了细粒度的局部对应信息**。例如，查询“一个人用右手画圈”时，全局嵌入难以精确捕捉“右手”这一局部语义与运动序列中特定关节轨迹之间的对应关系。

### 现有方法缺口：局部信息的系统性丢失

近年来，研究者尝试从多个角度提升运动检索的精度：

- **表示层面**：**MoPatch**（Yu et al., CVPR 2024）将运动序列编码为基于关节位置的伪图像，利用视觉Transformer（ViT）提取特征，但仍采用全局池化，未能充分利用ViT的patch级空间结构。
- **文本增强层面**：**CAR**（Fujiwara et al., ECCV 2024）和**SGAR**（Zhang et al., NeurIPS）等方法借助大语言模型（LLM）扩充文本描述，但这类策略增加了对额外模型的依赖，且未从根本上解决跨模态细粒度对齐问题。
- **语义对齐层面**：**KinMo**（Zhang et al., ICCV 2025）和**SECL**（Shi et al., ACM MM 2025）等方法引入了运动学感知或序列事件一致性学习，但其对齐机制仍以全局嵌入为基础。

**核心瓶颈**在于：现有方法将运动序列压缩为单一全局向量，导致**局部关节运动与文本词元之间的细粒度对应关系被完全淹没**。这不仅限制了检索精度的进一步提升，也使得检索结果缺乏可解释性——用户无法理解为何某段运动被检索到。

### 本文动机：从全局压缩到局部显式对齐

针对上述瓶颈，本文提出两条核心动机：

1. **设计保留局部结构的运动表示**：将运动序列转化为结构化的伪图像，使图像的每个空间区域天然对应特定身体关节，从而为细粒度对齐提供结构化基础。这要求运动表示能够解耦局部关节运动与全局轨迹，避免位置表示中不同关节运动相互纠缠的问题。

2. **引入显式的局部交互机制**：放弃全局池化，转而采用允许每个文本词元与最相关运动区块动态匹配的延迟交互策略，在保留局部信息的同时实现可解释的跨模态对齐。

这两条动机共同指向一个目标：**构建一个既能保持检索效率，又能提供细粒度、可解释对齐的文本-运动检索框架**。

## 核心方法与创新机理

### 瓶颈洞察：全局嵌入的细粒度信息丢失

现有文本-运动检索方法普遍采用双编码器架构（如 **TMR** (Petrovich et al., ICCV 2023)、**MoPatch** (Yu et al., CVPR 2024)），将运动序列和文本描述分别压缩为单一全局嵌入向量，通过余弦相似度进行匹配。这一范式存在根本性缺陷：运动序列中的局部关节动态（如“右手抬起”仅涉及肩、肘关节）和文本描述中的细粒度语义（如“缓慢地”、“高踢”）在全局池化过程中被不可逆地混合，导致跨模态对齐的精度和可解释性受限。

### 三大核心创新

MaxSim 围绕上述瓶颈，从运动表示、对齐策略和文本正则化三个维度进行了系统性创新，构成一个完整的细粒度检索框架。

#### 创新一：关节角度运动图像（Joint-Angle Motion Image）

**Changed Slot**: 运动表示，从原始 3D 关节位置或 6D 旋转特征 → 基于关节角度的结构化伪图像。

核心思想是通过运动学解耦，将局部关节运动与全局身体位移分离。具体而言，对每个骨骼关节通过逆运动学计算其在父关节局部坐标系中的屈伸角（flexion/extension）和内收外展角（adduction/abduction），公式为：

$$\theta_{\mathrm{flex}} = \mathrm{atan2}(\widetilde v_x, -\widetilde v_y), \quad \theta_{\mathrm{add}} = \mathrm{sign}(\widetilde v_z) \cdot \operatorname{arccos}\left( \frac{\widetilde v \cdot \widetilde v_{xy}}{\|\widetilde v\| \left\|\widetilde v_{xy}\right\|} \right)$$

每个关节的 29 维运动学特征经独立投影 $h_{t,k} = \phi_k(p_{t,k}) \in \mathbb{R}^{d_{part}}$ 后，沿时间轴堆叠并填充至 $T=224$，形成 $224 \times 224$ 的伪图像。**关键设计**：每个关节占据图像中的特定水平带（horizontal band），使 ViT 的每个 patch 天然对应一个特定关节的局部运动——这是后续 token-patch 细粒度对齐的结构基础。

消融实验（Table 3）验证了这一表示的优势：在 HumanML3D 上，关节角度表示结合 MaxSim 的 T2M R@5 比基于位置的表示提升 **+2.85%**，证实了运动学解耦对细粒度检索的因果贡献。

#### 创新二：MaxSim Token-Patch 延迟交互

**Changed Slot**: 对齐策略，从全局 [CLS] 嵌入的余弦相似度 → 基于 token-patch 最大相似度平均的延迟交互。

传统双编码器在编码阶段即完成跨模态融合（通过全局池化），而 MaxSim 将交互推迟到相似度计算阶段，保留完整的 patch 序列 $V = \{v_1, ..., v_N\}$ 和 token 序列 $L = \{l_1, ..., l_M\}$。相似度计算分为两步：

1. 构建 token-patch 交互矩阵 $S_{ij} = \frac{l_i \cdot v_j^T}{\|l_i\| \|v_j\|}$
2. 对每个文本 token 取最大 patch 相似度后平均：$\mathrm{Sim}(\mathcal{T}, \mathcal{M}) = \frac{1}{M} \sum_{i=1}^{M} \max_{j=1}^{N} (S_{ij})$

这一机制使每个文本词元（如“右腿”、“高踢”）能够动态匹配运动序列中最相关的局部区块，而非被迫与全局平均向量对齐。定性可视化（Figure 4）提供了直接证据：对于查询“右腿高踢”，交互热力图的激活区域集中于右髋、膝、踝关节的对应时间窗口，实现了语义级别的可解释对齐。

#### 创新三：掩码语言建模正则化

**Changed Slot**: 文本训练正则化，从无 MLM → 以 $\lambda_{mlm}=0.2$ 添加掩码语言建模辅助损失。

纯对比学习训练的文本编码器倾向于产生“词袋”式的 token 嵌入，缺乏句子级上下文信息，削弱了 MaxSim 中每个 token 独立匹配的语义质量。为此，引入 MLM 辅助损失：

$$\mathcal{L}_{mlm} = - \sum_{i \in \operatorname{mask}} \log P(w_i | \mathcal{T}_{masked}; \theta_{text})$$

总损失为 $\mathcal{L}_{total} = \mathcal{L}_{ret} + \lambda_{mlm} \mathcal{L}_{mlm}$。消融实验（Table 3）表明，在基于位置的表示上添加 MLM 正则化，使 HumanML3D 上的 T2M R@1 从 10.88% 提升至 **11.86%**，M2T R@1 从 11.82% 提升至 **12.93%**，且在 M2T 检索的 R@3（+2.18%）和 R@10（+2.15%）上增益尤为显著，说明上下文增强的 token 嵌入对运动到文本的匹配更为关键。

### 创新协同效应

三项创新并非孤立生效，而是形成正向协同：关节角度表示提供了关节级别的结构化 patch 分区，使 MaxSim 的 token-patch 匹配具有明确的物理语义；MLM 正则化则确保了参与匹配的文本 token 携带充分的上下文信息。三者共同实现了从“全局压缩匹配”到“局部可解释对齐”的范式转变。

MaxSim 提出了一套三阶段的文本-运动检索框架，其核心设计围绕**细粒度跨模态对齐**展开。整个 pipeline 由五个关键模块串联而成，形成从原始运动数据到最终检索分数的完整流。

### 输入与表示转换

框架的输入为一对自然语言描述 $\mathcal{T}$ 和人体骨骼运动序列。运动序列首先经过**关节角度提取与运动图像构建**模块：通过逆向运动学将原始骨骼数据转换为 29 维关节角度特征（覆盖 14 个关节），再将这些局部特征沿时间轴堆叠并填充至 $224 \times 224$ 分辨率，形成结构化的伪图像——**Motion Image**。该图像的水平条带与具体关节一一对应，使得后续 Vision Transformer 的每个 patch 自然承载特定关节的运动信息。

### 双编码器与特征保留

Motion Image 和文本描述分别进入两个独立的 Transformer 编码器：

- **Vision Transformer 运动编码器** $\mathcal{E}_m$ 将 Motion Image 编码为 $N$ 个 patch 嵌入 $V = \{v_1, v_2, ..., v_N\} \in \mathbb{R}^{N \times d}$；
- **Transformer 文本编码器** $\mathcal{E}_t$ 将文本描述编码为 $M$ 个 token 嵌入 $L = \{l_1, l_2, ..., l_M\} \in \mathbb{R}^{M \times d}$。

与 CLIP 风格的全局池化不同，MaxSim **保留完整的 patch/token 序列**，不将其压缩为单一的 [CLS] 向量，从而为后续的细粒度交互保留了局部信息。

### MaxSim 延迟交互

检索的核心是 **MaxSim 延迟交互**模块。对于任意文本-运动对，首先计算所有 token-patch 对的余弦相似度矩阵 $S_{ij}$，然后取每个文本 token 在所有运动 patch 上的最大相似度，最后对 $M$ 个 token 取平均，得到最终的匹配分数：

$$\mathrm{Sim}(\mathcal{T}, \mathcal{M}) = \frac{1}{M} \sum_{i=1}^{M} \max_{j=1}^{N} (S_{ij})$$

这种“延迟交互”策略使得检索分数在编码之后计算，既保留了局部对齐的细粒度信息，又支持候选嵌入的离线预计算——只有查询文本需要在线编码，候选运动库的 patch 嵌入可提前存储。

### 训练正则化

在训练阶段，框架额外引入 **MLM 正则化**模块：对文本编码器的输入进行随机掩码，并以掩码语言建模作为辅助任务，损失权重 $\lambda_{mlm} = 0.2$。该正则化强制文本 token 嵌入融入更丰富的句子级上下文信息，从而提升跨模态对齐的质量。

### 数据流总览

整体数据流可概括为：**原始运动 → 关节角度提取 → Motion Image → ViT 编码（保留 patch）→ 与文本 token 嵌入进行 MaxSim 交互 → 检索分数**。训练时，总损失由对称的批次内对比检索损失和 MLM 辅助损失共同构成：$\mathcal{L}_{total} = \mathcal{L}_{ret} + \lambda_{mlm} \mathcal{L}_{mlm}$。推理时，MLM 模块被移除，仅保留双编码器前向传播和 MaxSim 相似度计算。

> **需要手动验证**：三阶段训练的具体阶段划分（如是否包含预训练、微调、对齐等步骤）在提供的分析材料中未明确展开，建议查阅原文 Section 3.5 及 Figure 1 以确认各阶段的训练策略和参数设置。

![[assets/figures/papers/paper_list_l54_https_arxiv_org_pdf_2603_09930v1/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the three-stage training pipeline*

MaxSim 的检索框架由四个核心模块构成，分别负责运动表示、双塔编码、延迟交互对齐与文本正则化。以下逐一展开其设计逻辑与关键公式。

### 3.1 关节角度运动图像构建

现有方法直接使用原始 3D 关节位置或 6D 旋转特征，导致局部关节运动与全局身体位移耦合，难以实现细粒度对齐。MaxSim 的核心创新在于**通过逆运动学将骨骼运动序列转化为结构化的关节角度伪图像**，从表示层面解耦局部与全局运动。

对于球窝关节（ball-and-socket joint），给定子关节在父关节局部坐标系中的方向向量 $\widetilde{v}$，其屈伸角与内收外展角由下式分解：

$$
\theta_{\mathrm{flex}} = \mathrm{atan2}(\widetilde v_x, -\widetilde v_y), \quad \theta_{\mathrm{add}} = \mathrm{sign}(\widetilde v_z) \cdot \operatorname{arccos}\left( \frac{\widetilde v \cdot \widetilde v_{xy}}{\|\widetilde v\| \left\|\widetilde v_{xy}\right\|} \right)
$$

该公式将三维方向投影至父关节的两个正交运动平面，使每个关节的独立运动被显式编码为标量角度。对于铰链关节（如膝关节），仅保留单一屈伸角。最终，整个人体骨骼的 14 个关节被映射为 29 维运动学特征（见 Table 1），每帧的关节特征通过可学习投影映射至统一维度：

$$
h_{t,k} = \phi_k(p_{t,k}) \in \mathbb{R}^{d_{part}}
$$

其中 $d_{part}=16$，$t$ 为帧索引，$k$ 为关节索引。将所有帧沿时间轴堆叠并填充至 $T=224$，即得到尺寸为 $224 \times 224$ 的 **Motion Image** $I_{motion}$。该伪图像的每一水平条带对应一个特定关节，使 ViT 的每个 patch 天然与特定身体部位关联——这是后续 MaxSim 可解释对齐的结构性前提。

### 3.2 双塔编码与特征保留

与传统 CLIP 式双编码器不同，MaxSim **保留编码器的完整输出序列而非池化为单一全局向量**，这是实现 token-patch 延迟交互的基础。

- **运动编码器**：采用 Vision Transformer 作为骨干 $\mathcal{E}_m$，将 Motion Image 编码为 $N$ 个 patch 特征：

$$
V = \mathcal{E}_m(I_{motion}) = \{v_1, v_2, ..., v_N\} \in \mathbb{R}^{N \times d}
$$

- **文本编码器**：采用 Transformer 语言模型 $\mathcal{E}_t$，将文本描述 $T$ 编码为 $M$ 个 token 隐状态：

$$
L = \mathcal{E}_t(T) = \{l_1, l_2, ..., l_M\} \in \mathbb{R}^{M \times d}
$$

两个编码器的输出被投影至共享潜在空间，维度 $d=256$。序列长度 $N$ 和 $M$ 分别取决于 ViT 的 patch 划分策略与文本的 token 化长度。

### 3.3 MaxSim 延迟交互机制

MaxSim 的核心对齐策略是 **token-patch 延迟交互**：不将跨模态信息压缩为单个全局相似度，而是显式计算每个文本词元与每个运动区块之间的细粒度对应关系。

首先构建 token-patch 交互矩阵，计算所有文本词元 $l_i$ 与运动 patch $v_j$ 之间的余弦相似度：

$$
S_{ij} = \frac{l_i \cdot v_j^T}{\|l_i\| \|v_j\|}
$$

随后，对每个文本词元 $i$，取其与所有运动 patch 的最大相似度，并在所有词元上取平均，得到最终的检索相似度得分：

$$
\mathrm{Sim}(\mathcal{T}, \mathcal{M}) = \frac{1}{M} \sum_{i=1}^{M} \max_{j=1}^{N} (S_{ij})
$$

这一设计的直觉在于：**每个文本词元只需匹配运动序列中最相关的局部区块**，而非要求整个句子与整个运动全局一致。例如，查询“右腿高踢”时，“右腿”词元会自然激活右髋、膝、踝对应 patch 区域（见 Figure 4），而“高踢”词元则匹配相应时间段的运动幅度。这种“最大池化”式的对齐策略保留了局部运动细节，是检索精度和可解释性提升的关键因果机制。

![[assets/figures/papers/paper_list_l54_https_arxiv_org_pdf_2603_09930v1/figures/008_Figure_4.jpg]]
*Figure 4: MaxSim interaction score maps for two text-motion pairs. Left: 3D motion. Middle: normalized Motion Image. Right: interaction score map (brighter = stronger alignment)*

### 3.4 掩码语言建模正则化

纯对比学习训练可能导致文本编码器生成的词元嵌入过度依赖判别性关键词，而缺乏充分的句子级上下文信息。为解决这一问题，MaxSim 在训练阶段引入**掩码语言建模（MLM）**作为辅助正则化任务：

$$
\mathcal{L}_{mlm} = - \sum_{i \in \operatorname{mask}} \log P(w_i | \mathcal{T}_{masked}; \theta_{text})
$$

其中 $\mathcal{T}_{masked}$ 为随机掩码部分词元后的文本序列，模型需基于剩余上下文预测被掩码的词。该损失以权重 $\lambda_{mlm}=0.2$ 与检索损失联合优化：

$$
\mathcal{L}_{total} = \mathcal{L}_{ret} + \lambda_{mlm} \mathcal{L}_{mlm}
$$

$\mathcal{L}_{ret}$ 为对称的批内对比损失（in-batch symmetric contrastive loss）。消融实验表明（Table 3），MLM 正则化在 M2T 检索任务上增益尤为显著（R@3 +2.18%，R@10 +2.15%），因其强制文本编码器在词元级别编码更丰富的上下文语义，从而在反向检索中提供更强的判别力。

## 实验与关键发现

### 主实验结果

MaxSim 在 HumanML3D 和 KIT-ML 两个标准基准上均取得了领先的文本-运动跨模态检索性能。在 HumanML3D 数据集上，MaxSim 基础模型在 T2M 检索的 R@10 指标上达到 43.80%，相比采用全局池化的 **MoPatch**（Yu et al., CVPR 2024）提升 **+3.02%**；在 M2T 检索的 R@10 上达到 41.45%，提升 **+2.72%**（Table 4）。当扩展至 ViT-Large 与 RoBERTa-Large 骨干网络时（Ours-L），性能进一步提升，T2M R@10 达到 50.35%，显著优于所有未使用额外 LLM 文本增强的基线方法。在 KIT-ML 数据集上，基础模型在 T2M 检索中取得 R@10 59.28% 和 MedR 7.00 的最佳结果（Table 2）。

![[assets/figures/papers/paper_list_l54_https_arxiv_org_pdf_2603_09930v1/figures/004_Table_2.jpg]]
*Table 2: Comparison with state-of-the-art methods on HumanML3D and KIT-ML datasets. Ours-L uses ViT-Large and RoBERTa-Large backbones. †: methods used extra LLM augmentation text*

![[assets/figures/papers/paper_list_l54_https_arxiv_org_pdf_2603_09930v1/figures/007_Table_4.jpg]]
*Table 4: Efficiency and compression trade-off on HumanML3D. PQ: Product Quantization; Binary: asymmetric binary hashing. Query latency measured on a single NVIDIA H200 GPU*

值得注意的是，部分基线方法（标记为 †）使用了额外的大语言模型对文本描述进行增强，而 MaxSim 在未引入任何外部文本增强的条件下仍实现了可比甚至更优的性能，这验证了细粒度 token-patch 对齐机制本身的有效性。

### 消融实验

消融实验系统性地解耦了三个核心设计选择的影响：运动表示方式、检索对齐策略以及 MLM 正则化。

**关节角度表示 vs. 位置表示。** 在均采用 MaxSim 延迟交互的条件下，将基于位置的表示替换为关节角度表示后，HumanML3D 上 T2M R@5 提升 **+2.85%**（Table 3）。这一提升的根本原因在于关节角度表示天然地将每个关节的运动信息约束在 Motion Image 的特定水平带中，使 ViT 的每个 patch 与特定身体部位形成结构性对应关系，从而为 MaxSim 的 token-patch 对齐提供了更清晰的语义基础。相比之下，基于位置的表示中，同一关节在不同帧的位置变化可能散布于图像的任意区域，破坏了这种局部对应结构。

**MaxSim 延迟交互 vs. 全局池化。** 在关节角度表示下，MaxSim 延迟交互相比全局 [CLS] 嵌入的余弦相似度在 HumanML3D 上 T2M R@10 提升 **+3.02%**（Table 4）。这表明保留完整的 patch/token 序列并进行细粒度匹配，能够有效捕获全局嵌入所丢失的局部运动细节——这正是当前双编码器方法的瓶颈所在。

**MLM 正则化的增益。** 在基于位置的表示上添加 MLM 正则化后，HumanML3D 上 T2M R@1 从 10.88% 提升至 **11.86%**，M2T R@1 从 11.82% 提升至 **12.93%**（Table 3）。MLM 正则化在 M2T 方向上的增益尤为显著（R@3 +2.18%，R@10 +2.15%），这是因为掩码语言建模迫使文本编码器在每个词元的隐状态中注入更丰富的上下文信息，从而在运动检索文本时提供了更具判别力的查询表示。

### 可解释性分析

MaxSim 延迟交互机制天然产生可解释的 token-patch 对齐热力图。Figure 4 展示了两组文本-运动对的交互分数图，其中激活区域高度集中于与查询语义直接对应的身体关节和时间段。例如，当查询为“右腿高踢”时，热力图在右髋、右膝和右踝对应的空间带以及踢腿动作发生的时间段呈现显著激活。这种细粒度的对应关系不仅验证了关节角度表示的结构性优势，也为检索结果提供了直观的语义解释——用户可以明确看到模型的匹配依据是哪些身体部位和运动阶段。

### 效率与压缩分析

保留密集 patch 嵌入的代价是离线存储开销显著增加：浮点32位下约 837 MB，而全局嵌入仅需约 4 MB。为缓解这一问题，论文探索了后压缩方案。采用乘积量化（PQ，m=64）可实现 **16× 压缩**，且 T2M R@10 损失仅 ≤0.41%（Table 4）。在推理延迟方面，MaxSim 延迟交互（4.10 ms）相比全局池化（3.14 ms）仅增加约 1 ms，在保持细粒度对齐能力的同时未引入显著的计算负担。所有候选运动嵌入均可离线预计算，仅查询文本需在线编码，保证了实际部署的效率。

### 失败模式与局限性

尽管 MaxSim 在检索精度和可解释性上取得了显著提升，仍存在以下局限：

1. **存储开销**：密集 patch 嵌入的存储需求远高于全局嵌入方法，尽管 PQ 压缩可有效缓解，但在工业级大规模运动库（百万级以上）中仍需更高效的索引策略。
2. **任务范围限制**：本工作仅聚焦于文本-运动检索任务，关节角度表示和 MaxSim 对齐在运动生成、局部编辑或运动字幕生成等下游任务中的可迁移性尚未评估。
3. **复杂场景未验证**：当前实验基于单人运动的 HumanML3D 和 KIT-ML 数据集，对于多人交互或全身与物体交互等更复杂的运动场景，关节角度表示的有效性仍有待验证。

![[assets/figures/papers/paper_list_l54_https_arxiv_org_pdf_2603_09930v1/figures/006_Table_3.jpg]]
*Table 3: Ablation study of different feature representations, retrieval strategies and w/o Masked Language Modeling loss on HumanML3D and KIT-ML datasets*

![[assets/figures/papers/paper_list_l54_https_arxiv_org_pdf_2603_09930v1/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative T2M retrieval top-3 results on HumanML3D. Correct retrievals (ground-truth match) are highlighted in green*

## 定位与知识库关联

### 技术路线定位

MaxSim 处于**细粒度跨模态运动检索**这一新兴技术路线的核心位置。该路线的基本假设是：文本-运动检索的精度瓶颈不在于编码器的表征能力，而在于全局池化操作丢弃了局部对应信息。MaxSim 通过三个相互耦合的设计——关节角度运动图像、token-patch 延迟交互和 MLM 正则化——系统性地解决了这一问题。

从方法谱系来看，MaxSim 的直接前驱是 **MoPatch**（Yu et al., CVPR 2024），后者首次将运动序列重构为伪图像并引入 Vision Transformer 编码。然而，MoPatch 仍采用基于关节位置的表示和全局 [CLS] 池化，本质上延续了双编码器架构的信息压缩逻辑。MaxSim 的关键突破在于将“图像化”从编码便利性提升为**结构化对齐的载体**：关节角度表示使每个 patch 与特定关节建立一一对应关系，而 MaxSim 延迟交互则利用这种结构化特性实现词元级别的动态匹配。

与另一条技术路线——基于大语言模型增强的检索方法——相比，MaxSim 选择了不同的权衡。**CAR**（Fujiwara et al., ECCV 2024）和 **SGAR**（Zhang et al., NeurIPS）等方法通过 LLM 扩充文本描述来提升语义覆盖，但这引入了额外的推理开销和外部模型依赖。MaxSim 在未使用 LLM 增强的条件下，在 HumanML3D 上取得了与这些方法可比甚至更优的 T2M R@10（43.80%），表明**细粒度对齐机制本身可以弥补文本端的语义稀疏性**。

### 适用边界

MaxSim 的设计隐含了若干适用前提：

1. **骨架结构的一致性**：关节角度表示依赖于预定义的骨架拓扑（HumanML3D 和 KIT-ML 均基于 SMPL 骨架的 22 个关节）。对于具有不同关节数量或拓扑结构的运动数据，需要重新设计角度提取和 Motion Image 的 band 分配方案。

2. **文本描述需包含可定位的局部语义**：MaxSim 的优势来源于词元与关节/时间段的细粒度匹配。若文本描述高度抽象（如“一个人感到快乐”），缺乏可定位的局部动作线索，延迟交互的优势将减弱，退化为近似全局池化的效果。

3. **运动长度上限**：Motion Image 的宽度固定为 224 帧（约 11.2 秒 @ 20 fps），超出此长度的运动需要截断或降采样，可能丢失长时序依赖。对于需要完整上下文的长时间运动检索场景，该固定窗口构成硬性约束。

4. **离线存储敏感的场景需额外压缩**：保留 197 个 patch 嵌入（vs. 1 个全局嵌入）使存储开销增加约 200 倍（浮点32位下约 837 MB vs. 4 MB）。虽然乘积量化可将压缩比提升至 16× 且精度损失 ≤0.41%（Table 4），但在存储极度受限的边缘设备上仍需谨慎评估。

### 局限与开放问题

**已确认的局限**：

- **任务聚焦**：本工作仅验证了文本-运动检索任务，未评估所提表示和对齐机制在运动生成、运动编辑或运动字幕生成等下游任务中的迁移能力。关节角度表示是否能为这些任务提供更强的可控性，尚待实验验证。

- **多人类与交互场景未覆盖**：当前实验仅限于单人运动数据集。对于多人类交互或人与物体交互的运动，关节角度表示需要扩展到多骨架场景，且 Motion Image 的 band 分配策略需要重新设计。

- **检索效率的微小代价**：MaxSim 延迟交互的查询延迟（4.10 ms）略高于全局池化（3.14 ms），虽然绝对值较小，但在毫秒级延迟敏感的应用中仍需考虑。更关键的是，现有的近似最近邻搜索索引（如 IVF-PQ）通常针对单向量设计，如何为 MaxSim 的 token-patch 交互矩阵设计高效索引仍是一个开放问题。

**开放问题**：

- **工业级大规模运动库的索引策略**：当前方法依赖暴力搜索计算 token-patch 相似度矩阵。对于百万级运动库，如何设计支持细粒度交互的近似索引（如多向量索引或学习型哈希），是将其推向实际部署的关键挑战。

- **关节角度表示的可迁移性**：该表示的核心优势在于解耦局部与全局运动，这一特性理论上可惠及运动生成中的局部控制、运动修复中的缺失关节补全等任务，但需要针对性的适配和验证。

- **更丰富运动拓扑的泛化**：对于包含手部关节、面部表情或非人体骨架（如四足动物）的运动数据，关节角度表示能否保持其结构化和可解释性优势，需要进一步探索。

## 原文 PDF

![[paperPDFs/arxiv_2026/MaxSim_Fine_grained_Motion_Retrieval_via_Joint_Angle_Motion_Images_and_Token_Patch_Late_Interaction.pdf]]
