---
title: "MoGeFlow: Flowing Through Motion Codebook Geometry for Text-to-Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/MoGeFlow:_Flowing_Through_Motion_Codebook_Geometry_for_Text-to-Motion_Generation.pdf"
project_link: null
code_link: "https://github.com/PengchengFang-cs/MoGeFlow"
aliases:
- MoGeFlow
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将生成域从离散类别预测切换为在连续码书嵌入空间中的流匹配生成，并通过终端最近邻投影恢复到有效离散码序列以供冻结解码器使用。
primary_logic: 冻结的PartVQ运动码书嵌入空间存在可度量、非随机且解码器因果的几何结构：码间距与局部运动原型距离强相关，码替换引起的解码运动变化随码书距离单调递增。因此，在该几何空间中执行文本条件的连续流生成，既能保留离散解码接口的紧凑性与有效性，又能利用码书几何提升文本‑运动对齐与生成质量。
claims:
- 各部位码书中，码嵌入距离与对应局部运动原型距离的Spearman相关系数高，平均0.821，且随机打乱后消失（平均‑0.026），证明几何结构非随机。
- 替换码的距离越远，解码后的全身、目标组和局部变化越大，证明码书距离对解码运动具有因果效应。
- 在HumanML3D测试集上，MoGeFlow取得最高R‑Precision（Top‑1 0.592）和最佳MultiModal Distance（2.599），且在KIT‑ML上取得最佳R‑Precision和FID（0.130），MotionMillion上取得最佳R@1/2/3和FID。
- 消融实验中，用通用RVQ替换PartVQ接口大幅降低验证R@3和FID，而保持PartVQ接口的离散扩散基线也弱于MoGeFlow‑S，证明PartVQ几何接口与连续流先验互补。
---

# MoGeFlow: Flowing Through Motion Codebook Geometry for Text-to-Motion Generation

> [!tip] 核心洞察
> 冻结的PartVQ运动码书嵌入空间存在可度量、非随机且解码器因果的几何结构：码间距与局部运动原型距离强相关，码替换引起的解码运动变化随码书距离单调递增。因此，在该几何空间中执行文本条件的连续流生成，既能保留离散解码接口的紧凑性与有效性，又能利用码书几何提升文本‑运动对齐与生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoGeFlow：基于运动码书几何的文本到运动生成 |
| 英文题名 | MoGeFlow: Flowing Through Motion Codebook Geometry for Text-to-Motion Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2606.11656) · [Code](https://github.com/PengchengFang-cs/MoGeFlow) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MoGeFlow |
| Dataset | HumanML3D, KIT‑ML, MotionMillion |

> [!tip] 效果简介
> - HumanML3D (test set, repeat‑20) 上，R‑Precision Top‑1 ↑ 0.592±.002 vs SALAD 0.581±.003 (+0.011)；R‑Precision Top‑3 ↑ 0.867±.002 vs SALAD 0.857±.002 (+0.010)；MultiModal Distance ↓ 2.599±.008 vs SALAD 2.649±.009 (‑0.050)。
> - KIT‑ML (test set, repeat‑20) 上，R‑Precision Top‑1 ↑ 0.496±.003 vs SALAD 0.463±.003 (+0.033)；FID ↓ 0.130±.005 vs SALAD 0.208±.010 (‑0.078)。
> - MotionMillion (test set) 上，R@1 ↑ 0.91 vs ScaMo (previous best) (best reported)。

## 概要

文本到运动生成的核心挑战在于从自然语言描述合成高质量、语义对齐的三维人体运动序列。近年来，基于离散运动码的方法——先将运动压缩为离散令牌序列，再学习文本条件的生成先验——取得了显著进展。然而，这类方法的生成先验普遍将码书条目视为无序的类别标签，忽略了冻结运动码书嵌入空间中蕴含的物理运动几何结构，导致生成过程无法有效利用码间的邻近关系与解码器因果性。

本文提出 **MoGeFlow**，一种在连续码书嵌入空间中执行流匹配的文本到运动生成框架。其核心洞察在于：冻结的 PartVQ 运动码书嵌入空间存在可度量、非随机且解码器因果的几何结构——码间距与局部运动原型距离强相关（平均 Spearman 相关系数 0.821），且码替换引起的解码运动变化随码书距离单调递增。MoGeFlow 将生成域从离散类别预测切换为连续流匹配生成，在结构化运动码帧上学习文本条件的向量场，并通过终端最近邻投影恢复到有效离散码序列以供冻结解码器使用。这一设计既保留了离散解码接口的紧凑性与有效性，又充分利用码书几何提升文本-运动对齐与生成质量。

在 HumanML3D 测试集上，MoGeFlow 取得最高 R-Precision Top-1（0.592）和最佳 MultiModal Distance（2.599）；在 KIT-ML 上取得最佳 R-Precision 和 FID（0.130）；在 MotionMillion 上取得最佳 R@1/2/3 和 FID。消融实验进一步验证了 PartVQ 几何接口与连续流先验的互补性：用通用 RVQ 替换 PartVQ 接口大幅降低验证集 R@3（0.860→0.838）和 FID（0.081→0.169），而在相同 PartVQ 接口下，离散扩散先验的表现也弱于连续流先验。

### 文本到运动生成的核心挑战

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真、语义对齐的三维人体运动序列。该任务的核心瓶颈在于**运动表示**与**生成先验**之间的协同设计：运动表示决定了生成器操作的信息空间，而生成先验定义了如何在该空间中建模数据分布。

### 离散运动码先验的兴起与隐忧

近年来，基于矢量量化运动分词器（VQ-based Motion Tokenizer）的离散码方法在文本到运动生成领域取得了显著进展。这些方法将连续运动序列压缩为离散码序列，随后在离散码索引空间上训练生成先验。代表性工作包括：

- **T2M-GPT**（Zhang et al., CVPR 2023）：将运动生成建模为离散码的自回归预测任务。
- **MoMask**（Guo et al., CVPR 2024）：采用掩码建模策略在离散码空间上生成运动。
- **BAMM**（Pinyoanuntapong et al., ECCV 2024）：提出双向自回归框架处理运动码序列。
- **MoGenTS**（Yuan et al., NeurIPS 2024）：引入时空联合建模的运动码生成。
- **SALAD**（Hong et al., CVPR 2025）：在潜在空间中进行骨架感知的扩散生成。
- **MotionHiFlow**（Li et al., CVPR 2026）：采用分层流匹配进行文本到运动生成。

这些方法的共同特点是：**将运动码书条目视为无序的类别标签**，生成先验在离散索引空间（即类别空间）中操作。然而，这种设计隐含地丢弃了冻结运动码书嵌入空间中天然存在的几何结构——码嵌入之间的欧氏距离关系、邻近码之间的运动语义相似性，以及码替换对解码运动的因果效应。

### 冻结码书嵌入空间的几何结构被忽视

MoGeFlow的核心洞察在于：**冻结的PartVQ运动码书嵌入空间并非随机无序，而是存在可度量、非随机且解码器因果的几何结构**。具体而言：

1. **码嵌入距离与运动原型距离高度对齐**：在HumanML3D留出集上的诊断实验（Table 3）表明，六组码书中码嵌入距离与对应局部运动原型距离的Spearman相关系数平均高达0.821，而随机打乱码书后该相关性消失（平均-0.026），证明该几何结构非随机。

2. **码书距离对解码运动具有因果效应**：码替换诊断实验（Table 2(b)）显示，替换码的距离越远，解码后的全身、目标组和局部运动变化越大，表明码书距离对解码运动具有单调因果效应。

因此，**传统离散类别预测范式无法有效利用码书嵌入空间中的邻近关系与解码器因果性**，构成了现有方法的根本瓶颈。

### MoGeFlow的设计动机

MoGeFlow的设计动机源于一个关键问题：**能否在保留离散运动分词紧凑性与解码有效性的前提下，将生成域从离散类别预测切换到连续码嵌入空间，从而充分利用码书几何结构？**

为此，MoGeFlow提出了一种生成域转换策略：

- **生成域切换**：将生成先验从离散码索引空间（类别预测）迁移到连续码嵌入空间（流匹配），使生成过程能够感知码书几何。
- **终端投影恢复**：在生成管线末端通过最近邻投影将连续码帧恢复到有效离散码序列，供冻结解码器使用，确保解码接口的紧凑性与有效性。
- **结构化帧生成**：将同一时刻的各组码嵌入拼接为结构化运动码帧作为生成基本单元，而非孤立处理各组码标签。

这一设计使得MoGeFlow既能利用连续流匹配在几何感知空间中的建模能力，又能保留离散运动分词器的高效解码接口，从而在文本-运动对齐与生成质量上取得突破。

## 核心方法与创新机理

MoGeFlow 的核心创新可归结为一个**生成域的切换**：将文本条件运动先验从传统的**离散码索引空间（类别预测）**迁移至冻结运动码书的**连续嵌入空间（流匹配生成）**，并在终端通过最近邻投影恢复有效离散码序列以供冻结解码器使用。这一切换并非简单的表示变换，而是建立在对运动码书几何结构的系统诊断之上。

### 关键洞察：冻结码书嵌入空间存在可度量的几何结构

传统离散运动码先验（如 **T2M-GPT**（Zhang et al., CVPR 2023）、**MoMask**（Guo et al., CVPR 2024））将码书条目视为无序类别标签，忽略了码书嵌入空间中隐含的物理运动几何。MoGeFlow 的核心洞察在于：冻结的 PartVQ 运动码书嵌入空间具有**非随机、解码器因果的几何结构**。

具体而言，两项诊断实验确立了这一几何结构的两个关键属性：

**1. 码间距与运动原型距离强相关（非随机性）。** 对各部位码书，计算码嵌入间的欧氏距离与对应局部运动原型距离的 Spearman 相关系数 $\rho_p$，六组平均达到 **0.821**。作为对照，随机打乱码书索引后，该相关性消失（平均 **‑0.026**），证明该几何结构是码书学习过程中自然涌现的，而非随机噪声（Table 3）。

**2. 码替换对解码运动具有因果效应（解码器因果性）。** 将运动序列中的某一码替换为同组码书中的其他条目，替换码的距离越远，解码后的全身运动变化越大，且目标组和局部运动变化也呈现单调递增趋势（Table 2(b)）。这表明码书距离对解码运动具有可预测的因果影响，而非无关的潜在变量。

上述两个属性共同构成了 MoGeFlow 方法设计的理论前提：既然码书嵌入空间中存在可度量且解码器因果的几何结构，那么在该空间中执行文本条件的连续流生成，就能在保留离散解码接口紧凑性与有效性的同时，利用码书几何提升文本‑运动对齐与生成质量。

### 生成域切换：从离散类别到连续流匹配

基于上述洞察，MoGeFlow 对运动生成先验的三个关键环节进行了系统性改造：

| 变更维度 | 传统离散先验 | MoGeFlow 连续流先验 |
|----------|------------|-------------------|
| **生成域** | 离散码索引空间（类别预测） | 连续码嵌入空间（流匹配） |
| **生成单元** | 独立组码标签（孤立类别） | 结构化运动码帧（拼接各部组嵌入） |
| **训练目标** | 类别交叉熵/掩码建模损失 | 连续流匹配损失 |
| **终端解码** | 直接解码预测的类别索引 | 终端最近邻投影到冻结码书后解码 |

**结构化运动码帧**是生成单元的核心设计。MoGeFlow 将同一时刻的 $P$ 个部位组码嵌入拼接为一个帧向量 $\mathbf{y}_{1,t} = [q_{t,1}; q_{t,2}; \cdots; q_{t,P}] \in \mathbb{R}^{Pd}$，整个运动序列表示为帧序列 $\mathbf{Y}_1 \in \mathbb{R}^{T \times Pd}$。这使得生成的基本单元不再是孤立的部位索引，而是在几何空间中有明确位置的结构化帧状态。

**文本条件的连续流匹配**在码嵌入空间中定义 ODE 动态：

$$\frac{d\mathbf{Y}_\tau}{d\tau} = v_\theta(\mathbf{Y}_\tau, \tau, h(c)), \quad \tau \in [0,1]$$

其中 $v_\theta$ 为 Transformer 参数化的向量场，$h(c)$ 为文本条件嵌入。训练目标为流匹配损失 $\mathcal{L}_{\text{flow}}$，直接监督向量场在码嵌入空间中的位移方向。推理时从高斯噪声 $\mathbf{Y}_0 \sim \mathcal{N}(0,I)$ 出发，通过 ODE 积分得到连续帧状态 $\tilde{\mathbf{Y}}_1$。

**终端投影**将连续输出映射回离散码书以确保解码有效性：

$$\hat{z}_{t,p} = \arg\min_{k \in \{1,\dots,K_p\}} \|\tilde{q}_{t,p} - e_{p,k}\|_2^2$$

这一确定性硬分配机制使 MoGeFlow 能够在连续空间中自由生成，同时保证解码器接口的离散有效性。完整的生成管线为：

$$\mathbf{Y}_0 \sim \mathcal{N}(0,I),\ \tilde{\mathbf{Y}}_1 = \Phi_\theta^1(\mathbf{Y}_0; c),\ \hat{Z} = \Pi_{\mathcal{E}}(\tilde{\mathbf{Y}}_1),\ \hat{x} = D_\phi(\mathrm{Emb}_\mathcal{E}(\hat{Z}))$$

### 与现有方法的本质差异

MoGeFlow 与现有离散运动码方法的根本区别在于**生成域的选择**。**MoMask** 和 **T2M-GPT** 在离散标签空间中进行自回归或掩码生成，**BAMM**（Pinyoanuntapong et al., ECCV 2024）采用双向自回归，**MoGenTS**（Yuan et al., NeurIPS 2024）进行时空联合建模——这些方法均将码书条目视为无几何关系的类别。相比之下，MoGeFlow 将生成置于连续嵌入空间，使模型能够利用码书几何中的邻近关系来引导生成过程。

与连续运动生成方法（如 **MotionHiFlow**（Li et al., CVPR 2026）直接在运动数据空间进行流匹配，**SALAD**（Hong et al., CVPR 2025）在骨架感知的潜在空间扩散）相比，MoGeFlow 的独特之处在于其生成空间是**冻结码书的嵌入空间**——既非原始运动数据空间，也非通用潜在空间，而是一个已被证明具有解码器因果几何结构的特定表示空间。这使得 MoGeFlow 能够同时受益于离散分词器的紧凑性和连续流生成的几何感知能力。

消融实验（Table 4）直接验证了这一设计选择的必要性：在相同 PartVQ 接口下，离散类别扩散先验仅取得验证集 R@3 **0.826** / FID **0.083**，而 MoGeFlow‑S 的连续流先验达到 **0.860** / **0.081**，证明连续流更好地利用了码书几何。用通用 RVQ 替换 PartVQ 接口后，验证集 R@3 从 0.860 降至 **0.838**，FID 从 0.081 恶化至 **0.169**，表明 PartVQ 提供的结构化几何对性能至关重要。

MoGeFlow 的生成管线围绕一个核心洞察展开：冻结的运动码书嵌入空间中存在可度量、非随机且解码器因果的几何结构。基于此，MoGeFlow 将生成域从传统的离散类别预测切换到连续码嵌入空间中的流匹配生成，仅在终端通过最近邻投影恢复到有效离散码序列，供冻结解码器使用。整个管线由五个模块构成，数据流清晰且各模块职责分明。

**冻结的 PartVQ 运动分词器** 作为不可训练的基底，将原始运动序列映射到数据驱动的六组码嵌入。该分词器继承自 KV‑Control，其关节分组由统计发现而非人工预定义，六个组被描述性命名为 root、upper arms、right leg、upper neck、left leg 和 head。每个组拥有独立的码书（各含 128 个条目），组编码器 $E_\phi^p$ 将局部运动映射为潜在特征 $r_{t,p} \in \mathbb{R}^d$，经量化后得到组码嵌入 $q_{t,p}$。

**结构化运动码帧构造** 将同一时刻的六个组码嵌入拼接为一个帧向量，作为生成的基本单元：

$$\mathbf{y}_{1,t} = [q_{t,1}; q_{t,2}; \cdots; q_{t,P}] \in \mathbb{R}^{Pd},\quad \mathbf{Y}_1 = (\mathbf{y}_{1,1}, \dots, \mathbf{y}_{1,T}) \in \mathbb{R}^{T \times Pd}$$

这一设计使得生成单元不再是孤立的类别标签，而是一个在连续几何空间中演化的结构化帧。

**文本条件的流匹配 Transformer** 在码嵌入空间中学习从噪声到结构化帧端点的向量场。生成过程由文本条件 ODE 定义：

$$\frac{d\mathbf{Y}_\tau}{d\tau} = v_\theta(\mathbf{Y}_\tau, \tau, h(c)),\quad \tau \in [0,1]$$

其中 $h(c)$ 为文本嵌入条件。训练时，流匹配损失直接定义在连续码书嵌入空间上：

$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{(x,c),\mathbf{Y}_0,\tau}\left[\frac{1}{\sum m_t}\sum_{t=1}^T m_t\left\| v_\theta(\mathbf{Y}_\tau,\tau,h(c))_t - u_{\tau,t} \right\|_2^2 \right]$$

推理时，在速度域施加无分类器引导以增强文本条件：

$$\tilde{v} = v_\theta(\mathbf{Y}^n,\tau_n,h(\varnothing)) + s\left[v_\theta(\mathbf{Y}^n,\tau_n,h(c)) - v_\theta(\mathbf{Y}^n,\tau_n,h(\varnothing))\right]$$

**终端投影** 将 ODE 终端连续向量 $\tilde{q}_{t,p}$ 投影到各组冻结码书的最近邻条目，恢复有效离散码序列：

$$\hat{z}_{t,p} = \Pi_{\mathcal{E}_p}(\tilde{q}_{t,p}) = \arg\min_{k\in\{1,\dots,K_p\}}\|\tilde{q}_{t,p} - e_{p,k}\|_2^2$$

这一确定性硬分配确保了冻结解码器接收合法输入，但也意味着模型无法在终端保留多码不确定性——这是当前方法的一个内在局限。

**冻结的运动解码器** 从投影后的组码书嵌入重建全身运动，完成从文本到运动的端到端生成。

整体管线可概括为：

$$\mathbf{Y}_0 \sim \mathcal{N}(0,I),\ \tilde{\mathbf{Y}}_1 = \Phi_\theta^1(\mathbf{Y}_0; c),\ \hat{Z} = \Pi_{\mathcal{E}}(\tilde{\mathbf{Y}}_1),\ \hat{x} = D_\phi(\mathrm{Emb}_\mathcal{E}(\hat{Z}))$$

从噪声采样出发，经文本条件流生成连续码帧，终端投影到码书，最后冻结解码得到运动。这一设计的关键在于：连续流生成充分利用了码书嵌入空间的几何结构（码间距与局部运动原型距离强相关，Spearman 相关系数平均 0.821），而终端投影则保留了离散解码接口的紧凑性与有效性。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2606_11656/figures/001_Figure_1.jpg]]
*Figure 1: Overview of MoGeFlow. A frozen PartVQ tokenizer inherited from KV-Control maps motion into decoderbound code embeddings over data-derived joint groups, descriptively named root, upper arms, right leg, upper neck, left leg, and head. These groups are statistically discovered rather than manually predefined left/right or upper/lower body partitions. MoGeFlow learns a text-conditioned continuous flow over structured motion-code frames, projects terminal states to valid entries of each group-specific codebook, and decodes them with the frozen motion decoder*

MoGeFlow 的核心设计围绕一个关键因果操作展开：**将生成域从离散类别预测切换为冻结运动码书嵌入空间中的连续流匹配**，仅在终端通过最近邻投影恢复有效离散码序列。这一设计保留了离散分词器紧凑、有效的解码接口，同时使生成过程能够利用码书嵌入空间的几何结构。

### 冻结的PartVQ运动分词器

MoGeFlow 继承 KV‑Control 的冻结 PartVQ 分词器作为不可训练的基底。该分词器将运动序列映射到数据驱动的六个关节组，各组拥有独立的码书。组编码器定义为：

$$r_{t,p} = E_\phi^p(x_{\mathcal{T}_p})_t \in \mathbb{R}^d$$

其中 $x_{\mathcal{T}_p}$ 为第 $p$ 组关节的局部运动，$r_{t,p}$ 为时刻 $t$ 的潜在特征，经量化后得到组码嵌入 $q_{t,p}$。六个组由数据统计发现，描述性命名为 root、upper arms、right leg、upper neck、left leg、head，而非人工预定义的左右或上下半身划分。

### 结构化运动码帧

传统方法将各组码视为独立的类别标签，忽略了同一时刻不同组之间的结构关联。MoGeFlow 将同一时刻 $t$ 的 $P$ 个组码嵌入拼接为一个结构化帧向量，作为生成的基本单元：

$$\mathbf{y}_{1,t} = [q_{t,1}; q_{t,2}; \cdots; q_{t,P}] \in \mathbb{R}^{Pd}$$

整个运动序列的码帧表示为 $\mathbf{Y}_1 = (\mathbf{y}_{1,1}, \dots, \mathbf{y}_{1,T}) \in \mathbb{R}^{T \times Pd}$。这一构造使生成单元从孤立类别标签转变为具有内部几何结构的连续向量。

### 码书几何诊断

MoGeFlow 的核心洞察是：冻结的 PartVQ 码书嵌入空间存在**可度量、非随机且解码器因果的几何结构**。为验证这一点，论文定义了两项诊断指标。

**几何对齐性**：用 Spearman 相关系数量化各组码嵌入距离与对应局部运动原型距离的一致性：

$$\rho_p = \mathrm{Spearman}(\{D_p^\mathcal{E}(k,k')\}_{k<k'},\ \{D_p^\mathcal{M}(k,k')\}_{k<k'})$$

其中 $D_p^\mathcal{E}$ 为码嵌入间的欧氏距离，$D_p^\mathcal{M}$ 为对应局部运动原型间的距离。实验表明各组平均 $\rho_p = 0.821$，随机打乱码嵌入后降至平均 $-0.026$，证明几何结构非随机（Table 3）。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2606_11656/figures/006_Table_3.jpg]]
*Table 3: Motion codebook geometry diagnostics on held-out HumanML3D motions. Group-specific codebook distances align with local motion-prototype distances, while shuffled controls remove the alignment. The six groups are the data-derived PartVQ groups inherited from KV-Control and are descriptively named by their dominant joints. Each group codebook contains 128 entries*

**解码器因果性**：替换码的距离越远，解码后的全身、目标组和局部运动变化越大（Table 2(b)），证明码书距离对解码运动具有因果效应。

### 文本条件的流匹配

在码嵌入空间中定义文本条件的连续动态：

$$\frac{d\mathbf{Y}_\tau}{d\tau} = v_\theta(\mathbf{Y}_\tau, \tau, h(c)), \quad \tau \in [0,1]$$

其中 $h(c)$ 为文本条件嵌入，$v_\theta$ 为 Transformer 参数化的向量场。训练目标为流匹配损失，在连续码书嵌入空间中监督向量场的位移：

$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{(x,c),\mathbf{Y}_0,\tau}\left[\frac{1}{\sum m_t}\sum_{t=1}^T m_t\left\| v_\theta(\mathbf{Y}_\tau,\tau,h(c))_t - u_{\tau,t} \right\|_2^2 \right]$$

其中 $m_t$ 为有效帧掩码，$u_{\tau,t}$ 为目标速度场。该损失替代了传统离散码生成中的类别交叉熵或掩码建模损失。

### 终端投影与解码

流匹配生成的 ODE 终端状态 $\tilde{\mathbf{Y}}_1$ 为连续向量，需投影回各组冻结码书的最近邻条目以恢复有效离散码序列：

$$\hat{z}_{t,p} = \Pi_{\mathcal{E}_p}(\tilde{q}_{t,p}) = \arg\min_{k\in\{1,\dots,K_p\}}\|\tilde{q}_{t,p} - e_{p,k}\|_2^2$$

投影后的离散码 $\hat{Z}$ 经冻结运动解码器 $D_\phi$ 重建全身运动。完整的生成管线为：

$$\mathbf{Y}_0 \sim \mathcal{N}(0,I),\ \tilde{\mathbf{Y}}_1 = \Phi_\theta^1(\mathbf{Y}_0; c),\ \hat{Z} = \Pi_{\mathcal{E}}(\tilde{\mathbf{Y}}_1),\ \hat{x} = D_\phi(\mathrm{Emb}_\mathcal{E}(\hat{Z}))$$

### 无分类器引导

推理时在速度域施加无分类器引导以增强文本条件：

$$\tilde{v} = v_\theta(\mathbf{Y}^n,\tau_n,h(\varnothing)) + s\left[v_\theta(\mathbf{Y}^n,\tau_n,h(c)) - v_\theta(\mathbf{Y}^n,\tau_n,h(\varnothing))\right]$$

其中 $s$ 为引导强度，$h(\varnothing)$ 为空文本嵌入。

## 实验与关键发现

### 主要定量结果

MoGeFlow 在三个标准基准上进行了系统评估，均采用标准评测协议（HumanML3D/KIT‑ML 的 repeat‑20 评测，MotionMillion 的官方协议），汇报 95% 置信区间半宽。

**HumanML3D 测试集**（Table 1 上半部分）：MoGeFlow 在文本‑运动对齐指标上全面领先。R‑Precision Top‑1 达到 **0.592±.002**，较此前最优方法 **SALAD**（Hong et al., CVPR 2025）的 0.581±.003 提升 +0.011；Top‑3 为 **0.867±.002**，同样优于 SALAD 的 0.857±.002。MultiModal Distance 降至 **2.599±.008**，为所有方法中最低（SALAD 为 2.649±.009），表明文本与生成运动在联合嵌入空间中的匹配度最高。在运动质量方面，FID 为 **0.058±.003**，与 FID 最优的 **BAMM**（Pinyoanuntapong et al., ECCV 2024，0.055±.002）高度竞争，差距仅 +0.003，且在 R‑Precision 和 MM‑Dist 上显著优于 BAMM。Diversity 指标接近真实运动参考值，表明未出现模式坍塌。

**KIT‑ML 测试集**（Table 1 下半部分）：MoGeFlow 的优势更为突出。R‑Precision Top‑1 达到 **0.496±.003**，较 SALAD 的 0.463±.003 提升 +0.033；FID 降至 **0.130±.005**，较 SALAD 的 0.208±.010 大幅降低 −0.078，同时取得最佳 R‑Precision 和 FID，验证了方法在小数据集上的鲁棒性。

**MotionMillion 测试集**（Table 2(a)）：在大规模多样化基准上，MoGeFlow 取得最佳 R@1（**0.91**）、R@2、R@3 和 FID（**28.1**），均超越此前最优方法 ScaMo，证明码书空间流方法在开放域文本条件下的扩展能力。

### 运动码书几何诊断

MoGeFlow 的核心假设是冻结的 PartVQ 码书嵌入空间存在可度量且解码器因果的几何结构。Table 3 和 Table 2(b) 分别从相关性和因果性两个维度验证了这一假设。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2606_11656/figures/003_Table_2.jpg]]
*Table 2: Compact presentation of two additional results. Left: MotionMillion benchmark comparison under the MotionMillion evaluation protocol. Right: decoder-causal geometry diagnostic via code replacement, where farther codebook substitutions induce larger decoded motion changes*

**嵌入‑运动距离相关性**（Table 3）：对保留的 HumanML3D 运动，计算各组码书中码嵌入距离与对应局部运动原型距离的 Spearman 相关系数。六个数据驱动关节组（root、upper arms、right leg、upper neck、left leg、head）的平均相关系数为 **0.821**，表明码嵌入距离与物理运动差异高度一致。作为对照，随机打乱码‑运动对应关系后，平均相关系数降至 **−0.026**，排除了随机排列产生伪相关的可能。这证明 PartVQ 码书嵌入空间确实编码了有意义的运动几何结构。

**解码器因果性诊断**（Table 2(b)）：通过码替换实验验证码书距离对解码运动的因果效应。对给定运动序列的某一组码，用距离递增的替代码替换后解码，测量全身、目标组和局部运动的变化幅度。结果显示，替换码的距离越远，解码后的运动变化越大，且这一趋势在全身、目标组和局部三个尺度上均单调成立。这证明码书距离对下游解码运动具有因果影响，而非仅统计相关性。

### 消融实验

Table 4 在 HumanML3D 验证集上报告了关键消融结果，汇报各变体的最佳验证 R@3 和最佳 FID（可能来自不同检查点），作为验证包络的代表值。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2606_11656/figures/007_Table_4.jpg]]
*Table 4: Key ablations on HumanML3D validation. We report the best validation R@3 and best validation FID for each variant; the two values may occur at different checkpoints. Together, they summarize each variant’s validation envelope over training. Generic RVQ + flow tests the effect of replacing the PartVQ tokenizer interface, while Discrete Diffusion tests a categorical prior on the same PartVQ interface. Parameter counts refer to the trainable prior unless otherwise specified; the tokenizer and decoder are frozen during prior training*

**PartVQ 几何接口的必要性**：用通用 RVQ 替换 PartVQ 接口（Generic RVQ + flow）后，验证 R@3 从 MoGeFlow‑S 的 **0.860** 降至 **0.838**，FID 从 **0.081** 恶化至 **0.169**。这表明通用 RVQ 的码书缺乏 PartVQ 特有的组级几何结构，导致流匹配先验无法有效利用码间关系，性能大幅下降。

**连续流先验 vs. 离散扩散先验**：在相同 PartVQ 接口下，将连续流匹配替换为离散类别扩散先验（Discrete Diffusion），R@3 仅为 **0.826**，FID 为 **0.083**，均弱于 MoGeFlow‑S 的 0.860/0.081。这直接证明连续流生成能更好地利用码书嵌入空间的几何结构，而离散类别预测将码书条目视为孤立标签，损失了邻近关系信息。

**模型容量扩展**：增大可训练先验参数量（S→B→M→L），FID 持续改善（0.081→0.079→0.070→**0.058**），R@3 在 B 大小即接近饱和（0.870）。这表明更高运动质量分布需要更大模型容量，而文本‑运动对齐在中等容量下已基本收敛。最大变体 MoGeFlow‑L 的可训练参数为 690M，冻结的分词器和解码器不参与计数。

### 定性分析

Figure 2 展示了多阶段文本提示下的生成运动可视化对比。在“人向前走，然后坐下”等复合时序指令下，MoGeFlow 生成的骨骼序列能准确捕捉阶段过渡的时序边界和动作语义，而 **M‑Transformer**（Guo et al., 2022）和 **MoMask**（Guo et al., CVPR 2024）在阶段衔接处出现动作模糊或语义丢失。这归因于连续流生成在码书几何空间中的平滑演化，能够自然建模动作过渡，而离散自回归或掩码生成在类别边界处缺乏这种连续性先验。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2606_11656/figures/005_Figure_2.jpg]]
*Figure 2: Qualitative comparison on multi-stage text prompts. Each row shows one text condition, and each column shows one generated motion from MoGeFlow, M-Transformer (Guo et al., 2022), and MoMask (Guo et al., 2024). Motions are visualized by overlaying temporal skeleton poses on the ground plane; arrows indicate the global movement direction when visible*

### 局限性与待验证点

当前方法存在以下已知局限，需在应用中注意：

1. **冻结分词器的几何结构未优化**：PartVQ 分词器在训练流先验时保持冻结，其码书几何结构是预训练阶段的副产品，未针对流生成任务进行联合优化。这可能导致次优的几何空间用于流匹配。
2. **终端投影的信息损失**：最近邻投影为确定性硬分配，丢弃了连续输出与多个码书条目之间的不确定性关系，可能限制样本多样性——尽管 Diversity 指标接近真实分布，但在长尾或模糊文本条件下可能暴露不足。
3. **模型规模与部署成本**：最大变体 690M 可训练参数，虽在学术基准上取得最优结果，但实际部署时需权衡性能与推理开销。
4. **MotionMillion 结果的置信区间**：该基准的官方评测协议未要求重复采样汇报置信区间，Table 2(a) 的数值为单次评测结果，统计显著性需进一步验证。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2606_11656/figures/002_Table_1.jpg]]
*Table 1: Quantitative comparisons with recent representative and state-of-the-art methods on the HumanML3D (upper half) and KIT-ML (lower half) datasets. Symbol “±” denotes the half-width of the 95% confidence interval under the repeat-20 evaluation protocol. Text in bold and underline denotes the best and second-best generated-motion results for R-Precision, FID, and MultiModal Distance, respectively. Diversity is reported as a reference metric where values closer to real motion are preferred. Real motion is shown as a reference and is not included when ranking generated methods*

## 定位与知识库关联

### 1. 与基线方法的关系

MoGeFlow 的核心贡献在于**生成域的切换**：将文本到运动的生成从离散码索引空间迁移到冻结运动码书的连续嵌入空间，同时保留离散解码接口的紧凑性与有效性。这一设计使其与现有工作形成清晰的代际关系。

**离散运动码先验族**。以 **T2M-GPT**（Zhang et al., CVPR 2023）、**MoMask**（Guo et al., CVPR 2024）和 **BAMM**（Pinyoanuntapong et al., ECCV 2024）为代表的方法将运动分词为离散码序列，随后在类别标签空间上执行自回归或掩码生成。这些方法将码书条目视为无序类别，忽略了码嵌入空间中存在的物理运动几何结构。MoGeFlow 保留了相同的 PartVQ 分词器和冻结解码器接口，但将生成单元从孤立类别标签切换为**结构化运动码帧**——同一时刻六组码嵌入的拼接向量，从而在连续空间中执行流匹配生成。

**连续潜在空间生成族**。**SALAD**（Hong et al., CVPR 2025）在骨架感知的潜在空间中执行扩散生成，**MotionHiFlow**（Li et al., CVPR 2026）采用分层流匹配直接建模运动序列。MoGeFlow 与这些方法共享连续生成范式，但关键区别在于：MoGeFlow 的生成空间是冻结码书的嵌入空间，而非通用潜在空间。这一选择使得模型能够利用码书嵌入空间的几何结构——码间距与局部运动原型距离高度相关（平均 Spearman ρ = 0.821，Table 3），且码替换引起的解码运动变化随码书距离单调递增（Table 2b）——从而在保持离散解码有效性的同时获得几何感知的生成能力。

**时空联合建模族**。**MoGenTS**（Yuan et al., NeurIPS 2024）通过时空联合注意力建模运动序列。MoGeFlow 的流匹配 Transformer 同样在时空维度上操作，但其操作对象是结构化码帧向量，而非原始运动表示或通用潜在特征。

### 2. 适用边界

MoGeFlow 的适用性受以下设计选择约束：

- **冻结分词器依赖**：模型继承 KV-Control 的 PartVQ 分词器，关节分组由数据驱动发现（root、upper arms、right leg、upper neck、left leg、head），而非手动预定义的左右或上下半身划分。这意味着方法适用于该分词器能有效编码的运动类型，对于需要不同分组粒度的运动数据需重新训练分词器。
- **确定性终端投影**：推理时通过最近邻投影将连续输出映射到离散码书条目，该过程为硬分配，无法保留多个合理码之间的不确定性。对于需要高多样性的生成场景，这可能构成限制。
- **码书嵌入空间约束**：连续流生成仅在冻结码书的嵌入空间中定义，未扩展到更一般的潜在空间。分词器本身未针对几何特性进行联合学习，几何结构是冻结分词器的涌现属性而非优化目标。

### 3. 局限与开放问题

**已识别的局限**：

1. **分词器几何结构未优化**：当前模型使用冻结的 PartVQ 分词器，码书几何是训练后的静态属性。消融实验（Table 4）表明，用通用 RVQ 替换 PartVQ 接口后验证 R@3 从 0.860 降至 0.838、FID 从 0.081 恶化至 0.169，证明 PartVQ 的几何结构对性能至关重要。但该结构并非针对流匹配生成任务联合优化，可能存在进一步提升空间。

2. **终端投影的确定性瓶颈**：最近邻投影将连续向量唯一映射到单个码条目，丢失了邻近码之间的概率质量分布。这可能在文本条件模糊时限制生成多样性。

3. **模型规模与部署成本**：最大变体（MoGeFlow-L）拥有 690M 可训练参数，容量缩放实验（Table 4）显示 FID 持续改善（S→B→M→L: 0.081→0.079→0.070→0.058），但 R@3 在 B 大小即接近饱和（0.870），表明更高质量分布需要更大模型，可能增加实际部署成本。

**开放问题**：

1. **联合几何优化**：能否设计联合优化目标，使运动分词器在训练时主动增强解码器因果的几何结构？例如，在分词器训练中引入码书距离与运动距离的对齐损失，使几何结构从涌现属性变为显式优化目标。

2. **软投影机制**：能否采用软分配或混合投影机制，在终端投影时保留多码不确定性？例如，用 Gumbel-Softmax 或基于码书距离的加权组合替代确定性最近邻投影，可能提升生成多样性与鲁棒性。

3. **跨模态扩展**：码书空间流方法能否扩展到可控运动生成、交互式生成或多模态条件（音频-运动、视频-运动）？冻结码书嵌入空间作为统一的运动表示界面，理论上可接受不同模态的条件信号。

4. **高效架构设计**：更高效的流匹配架构（如线性注意力、状态空间模型）能否在减少参数量的同时保持或提升几何感知生成能力？容量缩放实验提示 FID 改善需要更大模型，但架构创新可能改变这一效率瓶颈。

## 原文 PDF

![[paperPDFs/arxiv_2026/MoGeFlow:_Flowing_Through_Motion_Codebook_Geometry_for_Text-to-Motion_Generation.pdf]]
