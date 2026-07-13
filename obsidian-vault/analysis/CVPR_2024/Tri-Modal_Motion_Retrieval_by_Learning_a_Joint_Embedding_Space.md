---
title: Tri-Modal Motion Retrieval by Learning a Joint Embedding Space
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Tri-Modal_Motion_Retrieval_by_Learning_a_Joint_Embedding_Space.pdf
project_link: null
code_link: null
aliases:
- LLVMA
- TMMRBLJES
tags:
- CVPR_2024
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 引入人体中心视频作为第三模态，利用视频在视觉和运动之间天然的紧密关联，以及视频-文本对齐数据的丰富性，缩小模态间语义鸿沟。
primary_logic: 通过三模态对比学习将文本、视频和运动对齐到同一嵌入空间，并设计以运动为查询的注意力融合机制，使运动重建能够从文本和视频中提取互补的语义信息，从而提升跨模态检索的准确性和鲁棒性。
claims:
- 在HumanML3D数据集上，引入视频模态的3-modal版本在文本-运动检索R@1上超过2-modal版本 (6.37 vs 5.93)，验证了第三模态的桥接作用。
- 在本论文新提出的视频-运动检索任务上，LAVIMO显著超越MotionCLIP和MotionSet等基线方法，证明了跨模态对齐的有效性。
- 用户研究显示，模型在真实人类视频上检索到主观相似3D运动的成功率达68.5%，展示了实际应用潜力。
- 定性结果（Figure 3）表明，模型能够准确检索到与文本或视频查询最匹配的运动序列，包括细粒度差异。
---

# Tri-Modal Motion Retrieval by Learning a Joint Embedding Space

> [!tip] 核心洞察
> 通过三模态对比学习将文本、视频和运动对齐到同一嵌入空间，并设计以运动为查询的注意力融合机制，使运动重建能够从文本和视频中提取互补的语义信息，从而提升跨模态检索的准确性和鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过学习联合嵌入空间的三模态运动检索 |
| 英文题名 | Tri-Modal Motion Retrieval by Learning a Joint Embedding Space |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2403.00691) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | LAVIMO (LAnguage-VIdeo-MOtion alignment) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R@1 (Text->Motion, All) 6.37 vs 5.68 (TMR) (+0.69)；R@1 (Text->Motion, Dissimilar) 30.00 vs 26.00 (TMR) (+4.00)；R@1 (Video->Motion, All) 21.25 vs MotionCLIP (具体值未在表格中提供) (显著提升)。
> - KIT-ML 上，R@1 (Text->Motion, All) 58.10 vs 49.25 (TMR) (+8.85)。

## 概要

文本到运动的跨模态检索面临一个根本瓶颈：文本描述与三维人体运动序列在语义空间中的距离过大，而高质量的文本-运动配对标注数据又十分稀缺，导致难以构建精准的联合嵌入空间。本文提出 **LAVIMO**（LAnguage-VIdeo-MOtion alignment），核心思路是引入人体中心视频作为第三模态，利用视频与运动之间天然的紧密视觉-运动关联，以及视频-文本对齐数据的相对丰富性，来桥接文本与运动之间的语义鸿沟。

LAVIMO 通过三模态对比学习将文本、视频和运动对齐到统一的嵌入空间，并设计了一个以运动为查询的注意力融合机制，使运动重建能够从文本和视频中提取互补语义信息。在 HumanML3D 和 KIT-ML 两个基准数据集上，LAVIMO 在文本-运动检索任务上超越了 **TMR**（Petrovich et al., ICCV 2023）等现有最优方法；在新提出的视频-运动检索任务上，也显著优于 **MotionCLIP**（Tevet et al., ECCV 2022）等基线。用户研究进一步表明，该框架在真实人类视频上检索到主观相似 3D 运动的成功率达 68.5%，展示了实际应用潜力。

> **公平性提示**：实验所用视频为基于 SMPL 模型动画渲染的合成 RGB 视频，与真实场景存在域差距；用户研究规模有限且未详细分析失败案例分布；代码未公开，可复现性依赖论文描述。

### 问题背景：文本-运动跨模态检索中的语义鸿沟

3D人体运动检索是计算机视觉与图形学中的基础任务，其核心挑战在于建立自然语言描述与人体运动序列之间的精准对应关系。然而，文本与运动这两种模态之间存在天然的语义鸿沟：文本是高度抽象、离散的符号序列，而运动则是连续、高维的时空轨迹。这一鸿沟导致直接将二者映射到同一嵌入空间时，模态间的距离过大，难以实现精确的跨模态匹配。

更关键的是，高质量文本-运动配对标注数据的稀缺进一步加剧了这一困难。与图像-文本等成熟的多模态领域相比，运动数据的采集和标注成本极高，使得现有方法在有限数据下难以学到足够鲁棒的联合表示。

### 现有方法的局限：双模态对齐的瓶颈

当前主流的文本-运动检索方法，如 **TEMOS** (Petrovich et al., ECCV 2022)、**MotionCLIP** (Tevet et al., ECCV 2022) 以及 **TMR** (Petrovich et al., ICCV 2023)，均采用双模态对比学习框架，试图将文本和运动直接对齐到共享嵌入空间。尽管 TMR 等最新工作在 HumanML3D 和 KIT-ML 等基准上取得了显著进展，但其性能提升已趋于平台期。

这一瓶颈的根源在于：双模态框架缺乏一个中间“桥梁”来弥合文本与运动之间的抽象层级差异。文本描述往往是高层语义的概括（如“一个人正在打拳”），而运动序列则包含大量细粒度的时空细节（如关节角度、速度、节奏）。仅凭文本-运动对的对比学习，模型难以捕捉这些细粒度对应关系，尤其是在训练数据有限的情况下。

### 核心动机：以视频为桥梁的三模态对齐

本文的核心洞察在于：**人体中心视频天然地同时与视觉外观和底层运动紧密关联**。视频帧记录了人体姿态的视觉呈现，而运动序列则是对这些姿态变化的结构化编码。因此，视频可以充当文本与运动之间的“语义桥梁”——文本与视频的对齐可以利用大规模视觉-语言预训练模型中蕴含的丰富知识，而视频与运动的对齐则可以通过渲染合成数据实现精确监督。

基于这一动机，本文提出 **LAVIMO (LAnguage-VIdeo-MOtion alignment)** 框架，首次将人体中心视频作为第三模态引入跨模态运动检索任务。通过三模态联合对比学习，LAVIMO 将文本、视频和运动同时对齐到一个统一的嵌入空间，并设计以运动为查询的注意力融合机制，使运动重建能够从文本和视频中提取互补的语义信息，从而提升跨模态检索的准确性和鲁棒性。

### 技术挑战与本文贡献

实现三模态对齐面临两个关键技术挑战：
1. **如何有效融合三个模态的信息**，使得运动表征能够从文本和视频中获取互补的语义线索；
2. **如何构造合适的训练目标**，避免因模态间语义相近但并非精确匹配的样本被错误地视为负样本而损害对齐质量。

针对上述挑战，LAVIMO 的主要贡献包括：
- 提出三模态联合嵌入框架，利用合成渲染视频扩展 HumanML3D 和 KIT-ML 数据集，实现文本-运动、视频-运动、文本-视频三对对齐；
- 设计基于 KL 散度的对比损失，结合语言模型相似度过滤的负样本筛选策略，提升对齐精度；
- 引入以运动为查询的多头注意力融合模块，在运动重建过程中自适应地从文本和视频中聚合信息；
- 在文本-运动检索和视频-运动检索两个任务上均取得最优性能，并通过用户研究验证了在真实人类视频上的实际应用潜力。

## 核心方法与创新机理

LAVIMO 的核心创新在于将人体中心视频作为第三模态引入文本-运动检索框架，通过三模态对比学习与运动查询的注意力融合机制，系统性地缩小了文本与运动之间的语义鸿沟。以下从三个关键维度拆解其相对于现有基线的创新点。

### 1. 三模态联合嵌入空间：视频作为语义桥梁

传统文本-运动检索方法（如 **TEMOS** (Petrovich et al., ECCV 2022)、**TMR** (Petrovich et al., ICCV 2023)）仅依赖文本与运动两种模态进行对齐，面临的根本瓶颈在于：文本与运动在嵌入空间中的距离过大，且高质量配对标注数据稀缺，导致难以建立精准的联合嵌入空间。

LAVIMO 的关键设计是将人体中心视频作为第三模态引入（Figure 1），利用视频在视觉与运动之间天然的紧密关联，以及视频-文本对齐数据的相对丰富性，构建文本-视频-运动三模态联合嵌入空间。这一设计的因果逻辑在于：

- **视频-运动关联**：视频帧序列直接记录了人体运动的视觉表现，与底层运动参数存在天然的对应关系；
- **视频-文本关联**：视觉-语言预训练模型（如 CLIP）已提供了较强的视频-文本对齐能力；
- **桥接效应**：视频模态在嵌入空间中充当“中间层”，通过分别与文本和运动对齐，间接拉近文本与运动之间的距离。

消融实验直接验证了这一设计的有效性：在 HumanML3D 数据集上，移除视频模态的 2-modal 版本（仅文本+运动）在文本-运动检索 R@1 上从 3-modal 版本的 6.37 降至 5.93（Table 1, Protocol All），证实了视频模态的桥接作用。在更具挑战性的 Dissimilar 协议下，3-modal 版本的 R@1 达到 30.00，显著优于 2-modal 版本的 26.00（Table 1c），表明视频模态在区分语义相近但不同的运动时尤为关键。

### 2. 基于 KL 散度的对比学习与负样本过滤

传统跨模态对比学习通常采用 InfoNCE 损失（如 CLIP 风格），将不同模态的正样本对拉近、负样本对推远。然而，在文本-运动检索场景中，不同文本描述可能语义相近（如“慢跑”与“跑步”），简单地将它们视为互斥的负样本会破坏嵌入空间的语义结构。

LAVIMO 对此进行了两项关键改进：

**（1）KL 散度对齐损失**：将对比学习重新定义为预测相似度矩阵与目标相似度矩阵之间的分布匹配问题。以文本-运动对齐为例，损失函数为：

$$\mathcal{L}_{align}^{mt} = KL(S_{pred}^{t2m}, S_{target}) + KL(S_{pred}^{m2t}, S_{target}^{\top})$$

其中 $S_{pred}$ 是模型预测的跨模态相似度矩阵，$S_{target}$ 是基于语言模型构造的目标相似度矩阵。这一设计使对齐目标从“硬性”的正/负样本区分转变为“软性”的相似度分布匹配，保留语义相近样本之间的关联。

**（2）基于语言模型的负样本过滤**：目标相似度矩阵 $S_{target}$ 通过预训练语言模型的余弦相似度构造，并引入阈值 $\epsilon$ 进行过滤：

$$S_{target}(i,j) = \begin{cases} \cos(\hat{e}_t^i, \hat{e}_t^j), & \text{if } \cos(\hat{e}_t^i, \hat{e}_t^j) \geq \epsilon \\ 0, & \text{otherwise} \end{cases}$$

低于阈值 $\epsilon$ 的文本对被视为语义无关，其目标相似度设为零；高于阈值的文本对保留其语义相似度，避免被错误地作为互斥负样本处理。这一技巧直接缓解了运动检索中“语义相近文本被错分为负样本”的核心问题。

### 3. 运动查询的跨模态注意力融合

传统方法（如 MotionCLIP）仅在编码器输出层进行全局特征对齐，运动重建过程独立于其他模态，无法利用文本或视频中的互补语义信息。

LAVIMO 设计了以运动为查询的特征融合模块（Features Fusion Module, Figure 2），其核心操作为：

$$\tilde{e}_m = Atten(Q_{e_m}, K_{e_m}, V_{e_m}) + Atten(Q_{e_m}, K_{e_t}, V_{e_t}) + Atten(Q_{e_m}, K_{e_v}, V_{e_v})$$

该模块以运动嵌入 $e_m$ 为查询，通过多头注意力分别从其自身、文本嵌入 $e_t$ 和视频嵌入 $e_v$ 中提取信息并求和，得到融合后的运动表示 $\tilde{e}_m$。融合后的特征随后输入运动解码器进行重建，并计算 MSE 重建损失。

这一设计的创新之处在于：

- **信息补偿**：当运动序列本身信息不完整或存在歧义时（如部分遮挡、噪声），运动查询可以从文本和视频中提取互补的语义信息来辅助重建；
- **模态协同**：注意力权重自动学习各模态对当前运动重建的贡献程度，实现动态的模态融合；
- **训练约束**：重建损失 $\mathcal{L}_{recon}$ 与对齐损失 $\mathcal{L}_{align}$ 联合优化（$\mathcal{L} = \mathcal{L}_{align} + \lambda_{recon} \cdot \mathcal{L}_{recon}$），确保融合特征既保持跨模态对齐性，又保留运动重建能力。

### 创新总结

| 创新维度 | 基线方法 | LAVIMO 改进 |
|---------|---------|------------|
| 模态组合 | 文本+运动 | 文本+视频+运动，视频桥接语义鸿沟 |
| 对比目标 | InfoNCE 硬性正/负样本区分 | KL 散度软性分布匹配 + 语言模型负样本过滤 |
| 信息融合 | 仅运动自重建 | 运动查询注意力从文本和视频聚合信息后重建 |
| 视频编码 | 无 | CLIP ViT-B/32 + 6层 temporal transformer |

这些创新共同作用，使 LAVIMO 在 HumanML3D 和 KIT-ML 两个基准上均超越 TMR 等现有最优方法，并首次在视频-运动检索任务上建立了有效的基线性能。

LAVIMO (LAnguage-VIdeo-MOtion alignment) 的核心设计动机源于一个关键瓶颈：文本与运动两种模态在嵌入空间中的语义距离过大，且高质量配对标注数据稀缺，导致难以建立精准的联合嵌入空间。为解决这一问题，LAVIMO 引入**人体中心视频作为第三模态**，利用视频在视觉外观与人体运动之间天然的紧密关联，以及视频-文本对齐数据的相对丰富性，在文本和运动之间架起一座语义桥梁。

### 三模态联合嵌入的整体流程

如图 Figure 1 所示，LAVIMO 的整体 pipeline 分为训练与推理两个阶段，三个模态各自通过独立的编码器提取特征，随后在统一的联合嵌入空间中通过对齐学习建立跨模态关联。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_00691/figures/001_Figure_1.jpg]]
*Figure 1: Overview of LAVIMO. During the training phase, the three modalities are processed through their distinct encoders. Subsequently, the resultant embeddings are aligned within a unified joint embedding space utilizing contrastive learning techniques. In the inference stage, the model is capable of accepting texts or videos as input queries, enabling the retrieval of corresponding motion data effectively*

**训练阶段**包含三个核心环节：

1. **模态编码**：文本、视频、运动三个模态分别输入各自的编码器，提取全局特征表示。文本编码器基于 DistilBERT，以 `[CLS]` token 的输出作为文本特征 $\boldsymbol{e}_t \in \mathbb{R}^{B \times C}$；运动编码器沿用 MotionCLIP 的 backbone，同样以 `[CLS]` token 输出作为运动特征 $\boldsymbol{e}_m$；视频编码器则基于 CLIP ViT-B/32（12层）叠加一个 6 层 temporal transformer，用于捕获帧序列的时空信息。

2. **跨模态对比学习**：三个模态的嵌入通过 KL 散度损失进行两两对齐，总对齐损失为三对之和：
   $$\mathcal{L}_{align} = \mathcal{L}_{align}^{mt} + \mathcal{L}_{align}^{mv} + \mathcal{L}_{align}^{tv}$$
   其中每对对齐损失（以文本-运动为例）衡量预测相似度矩阵与目标相似度矩阵之间的 KL 散度。目标矩阵通过预训练语言模型的余弦相似度构造，并引入阈值 $\epsilon$ 进行负样本过滤——低于阈值的样本对被置零，避免语义相近的文本被错误地当作负样本。

3. **特征融合与运动重建**：如 Figure 2 所示，特征融合模块以运动嵌入为查询（Query），通过多头注意力机制分别从运动自身、文本和视频中提取信息并求和，得到融合后的运动表示：
   $$\tilde{e}_m = Atten(Q_{e_m}, K_{e_m}, V_{e_m}) + Atten(Q_{e_m}, K_{e_t}, V_{e_t}) + Atten(Q_{e_m}, K_{e_v}, V_{e_v})$$
   该融合表示随后送入运动解码器进行重建，计算 MSE 重建损失。总训练损失为对齐损失与加权重建损失之和：
   $$\mathcal{L} = \mathcal{L}_{align} + \lambda_{recon} \cdot \mathcal{L}_{recon}$$

**推理阶段**，模型接受文本或视频作为查询，在联合嵌入空间中检索最匹配的运动序列。由于训练时三模态已被对齐到同一空间，跨模态检索可直接通过嵌入相似度完成。

### 关键设计选择

LAVIMO 相对于传统文本-运动双模态方法的三个核心改动槽位：

| 设计维度 | 基线方法 | LAVIMO 方案 |
|---------|---------|------------|
| 输入模态组合 | 文本 + 运动 | 文本 + 视频 + 运动 |
| 对比目标函数 | InfoNCE 损失（如 CLIP） | KL 散度损失 + 语言模型相似度过滤 |
| 运动重建中的多模态信息利用 | 仅基于运动自身重建 | 以运动为查询，通过注意力从文本和视频聚合信息后重建 |

其中，引入视频模态是最关键的架构创新——消融实验表明，移除视频模态（退化为 2-modal 版本）后，HumanML3D 上文本-运动检索的 R@1 从 6.37 降至 5.93，直接验证了第三模态的桥接作用。特征融合模块则使运动重建能够从文本和视频中提取互补语义，补偿运动模态本身可能缺失的信息，进一步强化了三模态之间的协同效应。

### 三模态编码器

LAVIMO 为文本、视频和运动三个模态分别设计编码器，将异构输入映射到统一的嵌入空间 $\mathbb{R}^{B \times C}$。

**运动编码器** 基于 MotionCLIP 构建，包含一个 6 层 Transformer 编码器。输入运动序列经线性投影后，在序列前端追加一个可学习的 `[CLS]` token，经 Transformer 处理后取第一个输出位置的向量作为全局运动特征 $\boldsymbol{e}_m \in \mathbb{R}^{B \times C}$。

**文本编码器** 采用 DistilBERT 作为基础模型。文本经分词后同样追加 `[CLS]` token，取 Transformer 编码器首位置输出作为文本特征 $\boldsymbol{e}_t \in \mathbb{R}^{B \times C}$。

**视频编码器** 是 LAVIMO 引入第三模态的关键模块。它基于 CLIP ViT-B/32（12 层）提取逐帧空间特征，再叠加一个 6 层 temporal transformer 对帧序列进行时序建模，最终获得视频的时空特征表示 $\boldsymbol{e}_v \in \mathbb{R}^{B \times C}$。

### 跨模态对比学习：KL 散度对齐

传统 InfoNCE 损失将同一 batch 内非配对样本统一视为负样本，在文本-运动对齐中容易将语义相近但非精确匹配的样本错误惩罚。LAVIMO 改用 KL 散度损失，并引入基于语言模型相似度的负样本过滤机制。

**总对齐损失** 由三对模态的对齐损失求和构成：

$$
\mathcal{L}_{align} = \mathcal{L}_{align}^{mt} + \mathcal{L}_{align}^{mv} + \mathcal{L}_{align}^{tv}
$$

以文本-运动对齐为例，先计算预测相似度矩阵。对于 batch 内第 $i$ 个文本嵌入 $\boldsymbol{e}_t^i$ 和第 $j$ 个运动嵌入 $\boldsymbol{e}_m^j$，文本到运动的预测相似度为：

$$
S_{pred}^{t2m}(i,j) = \frac{\exp(\cos(\boldsymbol{e}_t^i, \boldsymbol{e}_m^j) / \tau)}{\sum_{k=1}^B \exp(\cos(\boldsymbol{e}_t^i, \boldsymbol{e}_m^k) / \tau)}
$$

其中 $\tau$ 为温度系数。运动到文本的 $S_{pred}^{m2t}$ 按对称方式计算。

**目标相似度矩阵** 利用预训练语言模型构造，过滤语义不相关的负样本。对 batch 内任意两个文本嵌入 $\hat{\boldsymbol{e}}_t^i$ 和 $\hat{\boldsymbol{e}}_t^j$（来自冻结的预训练语言模型），目标矩阵定义为：

$$
S_{target}(i,j) = \begin{cases}
\cos(\hat{\boldsymbol{e}}_t^i, \hat{\boldsymbol{e}}_t^j), & \text{if } \cos(\hat{\boldsymbol{e}}_t^i, \hat{\boldsymbol{e}}_t^j) \geq \epsilon \\
0, & \text{otherwise}
\end{cases}
$$

低于阈值 $\epsilon$ 的文本对被视为无关，对应目标相似度置零，避免语义相近但非同一动作的文本被错误地作为负样本压制。

文本-运动对齐损失即为预测矩阵与目标矩阵的双向 KL 散度：

$$
\mathcal{L}_{align}^{mt} = KL(S_{pred}^{t2m}, S_{target}) + KL(S_{pred}^{m2t}, S_{target}^{\top})
$$

运动-视频 $\mathcal{L}_{align}^{mv}$ 和文本-视频 $\mathcal{L}_{align}^{tv}$ 的损失按相同形式计算。

### 特征融合模块：以运动为查询的跨模态注意力

Figure 2 展示了特征融合模块的架构。其核心思想是：运动嵌入可能缺失部分语义信息，通过注意力机制从文本和视频中提取互补信息来补偿。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_00691/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Features Fusion module. The embeddings for the text, video, and motion modalities are derived from their respective encoders. Subsequently, the motion embedding acts as a query to retrieve relevant information from the text and video, potentially compensating for any information that may be missing in the motion modality. The output of the attention mechanism is the weighted synthesis of the three modalities, which is then fed to the motion decoder for reconstruction*

具体地，以运动嵌入 $\boldsymbol{e}_m$ 为查询 $Q$，分别从运动自身、文本和视频中聚合信息：

$$
\tilde{\boldsymbol{e}}_m = \text{Atten}(Q_{\boldsymbol{e}_m}, K_{\boldsymbol{e}_m}, V_{\boldsymbol{e}_m}) + \text{Atten}(Q_{\boldsymbol{e}_m}, K_{\boldsymbol{e}_t}, V_{\boldsymbol{e}_t}) + \text{Atten}(Q_{\boldsymbol{e}_m}, K_{\boldsymbol{e}_v}, V_{\boldsymbol{e}_v})
$$

三项自注意力输出求和得到融合后的运动表示 $\tilde{\boldsymbol{e}}_m$。该表示随后送入运动解码器进行序列重建，重建损失为 MSE：

$$
\mathcal{L}_{recon} = \text{MSE}(\text{Decoder}(\tilde{\boldsymbol{e}}_m), \text{motion\_gt})
$$

### 总训练目标

最终训练损失为对齐损失与加权重建损失之和：

$$
\mathcal{L} = \mathcal{L}_{align} + \lambda_{recon} \cdot \mathcal{L}_{recon}
$$

其中 $\lambda_{recon}$ 控制重建损失的权重。这一联合优化目标同时约束三模态嵌入空间的对齐质量和运动表示的语义保真度。

## 实验与关键发现

### 文本-运动检索：三模态桥接的有效性

LAVIMO 在文本-运动检索任务上的核心主张是：引入人体中心视频作为第三模态，能有效缩小文本与运动之间的语义鸿沟。这一主张在 HumanML3D 和 KIT-ML 两个数据集上得到了定量验证。

在 HumanML3D 数据集上（Table 1），LAVIMO 的 3-modal 版本在 Protocol (a) All 下取得了 6.37 的 R@1（文本→运动），超越当前最优基线 **TMR**（Petrovich et al., ICCV 2023）的 5.68，提升 +0.69。关键的消融证据来自 2-modal 版本对比：移除视频模态后，R@1 从 6.37 降至 5.93，直接证实了视频模态的桥接作用。在更具挑战性的 Protocol (c) Dissimilar 设置下，3-modal 版本的 R@1 达到 30.00，较 TMR 的 26.00 提升 +4.00，表明模型在区分语义不相似样本时具有更强的判别力。

在 KIT-ML 数据集上（Table 2），LAVIMO 的优势更为显著：3-modal 版本的文本→运动 R@1 达到 58.10，较 TMR 的 49.25 提升 +8.85。值得注意的是，2-modal 版本在该数据集上已显著超越先前方法，而 3-modal 版本进一步拉大了差距。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_00691/figures/004_Table_2.jpg]]
*Table 2: Text-to-motion Retrieval on KIT-ML. We conduct further evaluations of both our 2-modal and 3-modal approaches using the KIT-ML dataset. The findings reveal that our 2-modal version significantly surpasses previous methodologies in performance. Moreover, our 3-modal version demonstrates an even greater extent of superiority over other existing methods. The most notable results are emphasized in bold*

这些结果共同指向一个因果机制：视频模态在视觉外观与运动之间天然具有紧密关联，同时视频-文本对齐数据相对丰富，因此在嵌入空间中充当了“语义桥梁”。当文本与运动的直接对齐因标注稀疏或描述歧义而困难时，视频提供了额外的约束信号。

### 视频-运动检索：新任务的基准建立

本文首次系统性地定义了视频-运动检索任务，并在 HumanML3D 和 KIT-ML 上建立了基准。LAVIMO 在该任务上显著超越 **MotionCLIP**（Tevet et al., ECCV 2022）和 **MotionSet**（Ren et al., IEEE Access 2020）等基线方法。

在 HumanML3D 上（Table 3），LAVIMO 在 Protocol (a) All 下视频→运动 R@1 达到 21.25。在 KIT-ML 上（Table 4），性能趋势一致，LAVIMO 以较大幅度领先。需要指出，MotionSet 最初并非为三模态跨模态检索设计，直接比较存在一定不公平性，但论文将其作为参考基线仍有参考价值。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_00691/figures/006_Table_3.jpg]]
*Table 3: Video-to-motion Retrieval on HumanML3D. We assess the video-to-motion retrieval task using the HumanML3D datasets. Our approach surpasses MotionCLIP [45] and MotionSet [39] across all the evaluation protocols in the table. The most notable results are emphasized in bold*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_00691/figures/007_Table_4.jpg]]
*Table 4: Video-to-motion Retrieval on KIT-ML. We assess the video-to-motion retrieval task using the KIT-ML datasets. Our findings align with those obtained from the HumanML3D, indicating that our framework significantly outperforms the performance of Motion-CLIP [45] and MotionSet [39] by a considerable margin*

用户研究进一步验证了实际应用潜力：在真实人类视频上进行视频→运动检索，模型检索到主观相似 3D 运动的成功率达 68.5%。该评估基于小规模人工标注，失败案例的分布和典型失败模式未在论文中详细说明，需要手动验证。

### 定性分析：细粒度检索能力

Figure 3 展示了定性对比结果。在文本→运动检索中，LAVIMO 能够准确检索到与查询文本最匹配的运动序列，例如对 “karate type motion” 类查询，正确检索到 ground-truth 运动，而 TMR 仅在 rank-3 才匹配到正确结果。在视频→运动检索中，模型不仅对合成测试视频表现良好，对真实场景视频也展示了泛化能力，检索到的运动与视频内容的语义一致性较高（如 “leg swinging”、“standing up and walking”）。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_00691/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative Comparison on the HumanML3D Dataset. Our method successfully performs text-to-motion and video-to-motion retrieval tasks. For text-to-motion retrieval, we compare our results with TMR [31]. In the first row, using a random text from the test set, our method accurately retrieves the correct motion at rank 1, with similar motions such as “boxing” at ranks 2 and 3, resembling ’‘karate type motion”. In contrast, TMR struggles, with only its rank 3 motion matching the ground truth. In the second row, when testing with a non-test set text involving “dance”, our model retrieves motions suggesting a “Latin dance”, more accurate than TMR’s less precise dance motions. For video-to-motion...*

### 公平性与局限性说明

实验所用的视频数据是通过动画和渲染 SMPL 人物生成的合成 RGB 视频，与真实场景视频存在域差距。用户研究的 68.5% 成功率虽然积极，但小规模评估的统计可靠性有限。此外，论文未提供代码链接，实验结果的可复现性依赖于论文中的实现细节描述。部分基线方法（如 MotionSet）并非为三模态跨模态检索设计，直接数值比较时需注意这一背景。

## 定位与知识库关联

### 从双模态到三模态的跨模态运动检索演进

LAVIMO 的核心贡献在于将运动检索从“文本-运动”双模态对齐推进到“文本-视频-运动”三模态联合学习，其方法谱系可沿两条线索追溯。

**文本-运动检索基线。** 该方向经历了从 VAE 到 CLIP 范式的发展。**TEMOS**（Petrovich et al., ECCV 2022）采用 VAE 框架进行文本条件运动生成，其编码器可兼用于检索。**Guo et al.**（CVPR 2022）和 **MotionCLIP**（Tevet et al., ECCV 2022）将 CLIP 的对比学习范式引入运动域，前者关注文本-运动匹配，后者通过 CLIP 图像空间桥接文本与运动。当前最优方法 **TMR**（Petrovich et al., ICCV 2023）进一步优化了对比目标。这些方法的共同瓶颈在于：文本与运动两种模态在嵌入空间中的语义鸿沟过大，且高质量配对标注数据稀缺，限制了联合嵌入空间的精度。

**视频-运动检索基线。** 该任务本身即由本文首次系统定义，此前仅有 **MotionSet**（Ren et al., IEEE Access 2020）等少量工作涉及，且并非为跨模态检索设计，直接比较存在公平性争议。

### LAVIMO 的方法定位与关键设计变更

LAVIMO 在上述谱系中的定位是**首个三模态联合对齐的运动检索框架**，其核心因果机制为：引入人体中心视频作为第三模态，利用视频与运动间天然的时空紧密关联（同一运动可同时呈现为 3D 骨架序列和 RGB 视频），以及视频-文本对齐数据的相对丰富性，缩小文本与运动间的语义鸿沟。

与基线相比，LAVIMO 在四个关键设计槽位上进行了变更：

| 设计槽位 | 基线方案 | LAVIMO 方案 | 变更动机 |
|---------|---------|------------|---------|
| 输入模态组合 | 文本+运动 | 文本+视频+运动 | 视频桥接文本与运动，提供互补语义信息 |
| 对比目标函数 | InfoNCE（如 CLIP） | KL 散度 + 语言模型负样本过滤 | 避免语义相近文本被错分为负样本，提升对齐精度 |
| 运动重建机制 | 仅基于运动自身重建 | 以运动为查询的跨模态注意力融合后重建 | 从文本和视频中提取互补信息补偿运动缺失 |
| 视频编码器 | 无 | CLIP ViT-B/32 + 6 层时序 Transformer | 提取视频帧序列的时空特征 |

其中，**KL 散度损失配合语言模型负样本过滤**（Eq. 6）是方法层面的重要创新：利用预训练语言模型的余弦相似度构造目标相似度矩阵，低于阈值 $`\epsilon`$ 的样本对设为 0，避免“慢跑”和“跑步”等语义相近文本在对比学习中被错误排斥。这一设计直接回应了文本-运动对齐中负样本定义模糊的难题。

**特征融合模块**（Eq. 7）以运动嵌入为查询 $`Q_{e_m}`$，通过多头注意力分别从文本 $`K_{e_t}, V_{e_t}`$ 和视频 $`K_{e_v}, V_{e_v}`$ 中聚合信息，再与运动自注意力输出求和，得到融合表示 $`\tilde{e}_m`$。这一设计使运动重建能够利用文本的语义先验和视频的视觉细节，形成三模态间的协同效应。

### 适用边界与局限

**数据依赖性。** 训练所用的视频数据是通过动画和渲染 SMPL 人物生成的合成 RGB 视频，与真实场景视频存在分布差距。用户研究虽展示了 68.5% 的真实视频检索成功率，但评估规模有限，且失败案例的分布未明确报告，实际部署时的泛化能力需进一步验证。

**模态依赖与计算开销。** 三模态架构在推理时需同时编码视频和文本，相比纯文本查询的基线增加了视频编码的计算成本。此外，视频编码器基于 CLIP ViT-B/32，其视觉表征偏向静态外观，对细粒度时序动作的捕捉能力受限于 6 层时序 Transformer 的设计。

**评估公平性。** 部分基线（如 MotionSet）最初并非为三模态跨模态检索设计，直接比较可能不完全公平，但论文仍将其作为参考基线，其性能差距的解读需谨慎。

### 开放问题

1. **真实场景泛化**：如何缩小合成渲染视频与真实人类视频之间的域差距，提升在自然场景中的检索鲁棒性？
2. **规模扩展**：三模态对齐框架能否扩展到更大规模的视频-文本-运动数据集，并迁移至运动生成、运动预测等更复杂的下游任务？
3. **注意力机制优化**：当前特征融合采用全局注意力，是否可引入细粒度的时空注意力（如在帧级别或关节级别进行跨模态对齐）以进一步提升精度？
4. **多模态扩展**：是否可利用音频、深度图等辅助模态进一步丰富跨模态对齐，构建更通用的运动理解框架？

需要指出的是，本文未提供代码链接，实验结果的可复现性限于论文描述，部分结论的独立验证存在困难。

## 原文 PDF

![[paperPDFs/CVPR_2024/Tri-Modal_Motion_Retrieval_by_Learning_a_Joint_Embedding_Space.pdf]]
