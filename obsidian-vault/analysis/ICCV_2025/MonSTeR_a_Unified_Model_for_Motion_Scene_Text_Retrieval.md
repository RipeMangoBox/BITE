---
title: "MonSTeR: a Unified Model for Motion, Scene, Text Retrieval"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/MonSTeR_a_Unified_Model_for_Motion_Scene_Text_Retrieval.pdf
code_link: https://github.com/colloroneluca/MonSTeR
project_link: https://github.com/colloroneluca/MonSTeR
aliases:
- MonSTeR
tags:
- ICCV_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过引入跨模态编码器，将单模态与成对模态的表示进行对比对齐，显式建模三模态之间的高阶交互关系。"
primary_logic: "将文本、运动、场景视为拓扑三角形，对齐节点（单模态表示）与边（成对跨模态表示），从而在统一潜在空间中捕捉三者之间的高阶依赖，实现灵活且鲁棒的多任务三模态检索。"
claims:
- "MonSTeR 在 HUMANISE+ 小批量协议上平均 mRecall 达到 60.00，比最强场景感知基线 TMR+S 提升 26.5%。"
- "在 HUMANISE+ 全量协议上，MonSTeR 平均 mRecall 达到 4.80，比最强场景感知基线 TMR+S 提升 76.5%。"
- "移除单模态对比损失导致 HUMANISE+ 小批量协议平均 mRecall 从 60.00 骤降至 41.77，证明单模态表示对于跨模态检索不可或缺。"
- "移除跨模态对比损失亦使平均 mRecall 下降至 56.07，表明跨模态对齐对提升双模态到单模态检索十分关键。"
---

# MonSTeR: a Unified Model for Motion, Scene, Text Retrieval

> [!tip] 核心洞察
> 将文本、运动、场景视为拓扑三角形，对齐节点（单模态表示）与边（成对跨模态表示），从而在统一潜在空间中捕捉三者之间的高阶依赖，实现灵活且鲁棒的多任务三模态检索。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MonSTeR：统一的运动、场景、文本检索模型 |
| 英文题名 | MonSTeR: a Unified Model for Motion, Scene, Text Retrieval |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2510.03200) · [GitHub](https://github.com/colloroneluca/MonSTeR) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | MonSTeR |
| Dataset | HUMANISE+ (All Protocol), HUMANISE+ (Small Batches Protocol), TRUMANS+ (All Protocol), TRUMANS+ (Small Batches Protocol) |

> [!tip] 效果简介
> - HUMANISE+ (All Protocol) 上，平均 mRecall@1,2,3,5,10 为 4.80，对比 2.72 (TMR+S)，变化 +76.5%。
> - HUMANISE+ (Small Batches Protocol) 上，平均 mRecall@1,2,3,5,10 为 60.00，对比 47.44 (TMR+S)，变化 +26.5%。
> - TRUMANS+ (All Protocol) 上，平均 mRecall@1,2,3,5,10 为 7.42，对比 5.49 (TMR+S)，变化 +35.1%。

## 概要

人类运动检索与评估长期聚焦于文本-运动对齐，忽略了场景上下文对运动意图的约束。现有方法无法评估文本、运动、场景三者的整体一致性，导致检索结果可能与物理环境冲突——例如，文本要求“坐到椅子上”，但场景中根本不存在椅子。

MonSTeR 提出将文本、运动、场景视为拓扑三角形，通过同时对齐节点（单模态表示）与边（成对跨模态表示），在统一潜在空间中捕捉三者之间的高阶依赖关系。其核心机制是引入跨模态编码器，将单模态与成对模态的表示进行对比对齐，从而显式建模三模态之间的高阶交互。

在 HUMANISE+ 数据集上，MonSTeR 在全量协议下平均 mRecall 达到 4.80，比最强场景感知基线 TMR+S 提升 76.5%；在小批量协议下达到 60.00，提升 26.5%。消融实验表明，单模态对比损失和跨模态对比损失对性能均不可或缺——移除任一组分都会导致显著下降。此外，MonSTeR 的检索评分与人类偏好的对齐准确率达到 66.5%，证明其能有效评估生成运动的质量。

MonSTeR 的局限在于：跨模态编码器仅在已对齐的模态对上训练，未能利用未配对数据；场景被假设为静态点云，无法建模人类动作对环境的动态改变。

### 人类运动理解的模态缺口

人类运动检索与生成是计算机视觉与图形学中的核心问题，其应用涵盖角色动画、人机交互、具身智能等领域。近年来，基于文本的运动检索（text-to-motion, t2m）与运动到文本检索（motion-to-text, m2t）取得了显著进展，代表性方法如 **TMR**（Petrovich et al., ICCV 2023）和 **MoPa**（Yu et al., CVPR 2024）通过对比学习将文本和运动映射到共享潜在空间，实现了高效的跨模态检索。

然而，这些方法存在一个根本性的盲区：**它们仅关注文本与运动之间的对齐，完全忽略了场景上下文对运动意图的约束**。在真实世界中，人类运动并非在真空中发生——“走向椅子坐下”这一动作的语义，只有在场景中确实存在一把可坐的椅子时才是完整且合理的。现有的文本-运动检索范式无法区分“在有空椅子的场景中走向椅子坐下”和“在没有椅子的场景中做出相同的走向动作”，因为模型从未学习过场景这一关键模态。

### 现有方法的局限

当前处理场景与运动关系的工作大致分为两类：

1. **纯文本-运动模型**（如 TMR、MoPa）：完全不编码场景信息，无法评估运动与场景的一致性，更无法执行场景感知的检索任务。
2. **场景感知的扩展变体**（如 TMR+S、MoPa+S）：在原有文本-运动模型的基础上附加场景编码器，但仅实现了浅层的模态拼接或简单的特征融合，**未能显式建模文本、运动、场景三者之间的高阶交互关系**。

这种高阶交互的缺失意味着模型无法捕捉“文本描述的运动意图是否与场景布局兼容”这一核心约束。例如，文本“绕过桌子走向门口”要求运动轨迹与场景中的桌子位置、门口方向保持一致，而不仅仅是文本与运动的语义匹配。

### 三模态一致性评估的挑战

将场景引入运动检索带来了一个更深层的问题：**如何在一个统一的框架中评估文本、运动、场景三者的整体一致性？** 这不是简单的三个成对相似度求和问题。从拓扑学的角度看，三模态关系 $\{t, m, s\}$ 的完整表示需要同时包含单模态表示 $\{t, m, s\}$ 和成对跨模态表示 $\{st, mt, ms\}$。缺失任何一个维度，都会导致潜在空间无法捕捉某些高阶依赖——例如，仅靠 $t$-$m$ 和 $m$-$s$ 的对齐，无法保证 $t$-$s$ 的一致性。

此外，现有数据集也存在标注缺陷。原始 HUMANISE 和 TRUMANS 数据集的文本标注通常缺乏场景上下文信息（例如仅标注“走向椅子”而不提及场景中椅子的具体位置或周围物体），这使得训练场景感知模型时缺乏高质量的监督信号。

### 本文动机

针对上述缺口，本文提出 **MonSTeR**（Motion, Scene, Text Retrieval），一个统一的三模态检索框架。MonSTeR 的核心动机是：**将文本、运动、场景视为一个拓扑三角形，通过对齐节点（单模态表示）与边（成对跨模态表示），在统一潜在空间中显式捕捉三者之间的高阶依赖**。这一设计使得模型不仅能够执行传统的 t2m 和 m2t 检索，还能灵活支持场景感知的检索任务（如 scene-text to motion, st2m；motion-scene to text, ms2t），以及运动质量评估等下游应用。

## 核心方法与创新机理

MonSTeR 的核心创新在于将**文本、运动、场景**三模态检索问题建模为一个**拓扑三角形**，并通过对齐三角形的“节点”（单模态表示）与“边”（成对跨模态表示）来捕捉三者之间的高阶依赖关系。这一设计直接回应了现有方法的关键瓶颈：**忽略场景上下文导致无法评估文本-运动-场景的整体一致性**。

### 从双模态到三模态的拓扑分解

现有基线如 **TMR**（Petrovich et al., ICCV 2023）和 **MoPa**（Yu et al., CVPR 2024）仅处理文本与运动的双模态对齐，缺乏对场景信息的编码能力。即使将其扩展为场景感知变体 **TMR+S** 和 **MoPa+S**，也仅是简单拼接场景编码，并未显式建模三模态之间的高阶交互。

MonSTeR 的因果调控旋钮在于：将三模态关系 $\{t, m, s\}$ 显式分解为单模态节点 $\{t, m, s\}$ 与成对跨模态边 $\{st, mt, ms\}$，并通过对比学习同时对齐节点与边。这一分解的理论依据来自拓扑学：表示三向关系需要同时表示单模态与成对跨模态项。

### 三个关键 changed slots

| 模块 | 基线值 | MonSTeR 方案 | 作用 |
|------|--------|-------------|------|
| **场景模态编码器** | 无（TMR/MoPa 仅处理文本和运动） | 基于点云的 Transformer VAE 编码器，将彩色点云场景编码为潜在向量 $v_s$ | 首次将场景上下文纳入统一检索空间 |
| **跨模态编码器** | 无 | 三个成对跨模态编码器（ST, MT, MS），通过拼接单模态标记生成联合潜在向量 $v_{st}, v_{mt}, v_{ms}$ | 显式建模双模态联合表示，作为“边”参与对齐 |
| **对比对齐目标集** | 仅文本-运动对齐（TMR/MoPa） | 六项组合 $K = \{(t,s), (m,t), (m,s), (st,m), (mt,s), (ms,t)\}$ | 同时对齐节点-节点、节点-边，防止模态坍塌 |

### 损失函数设计

总对比损失对预设集合 $K$ 中的每一对嵌入计算 InfoNCE 损失并取平均：

$$\mathcal{L}_{\mathrm{tot}} = \frac{1}{|K|} \sum_{(i,j) \in K} \frac{\mathcal{L}_{\mathrm{NCE}}(C_{i,j})}{N}$$

其中 $C_{i,j}$ 为模态对 $(i,j)$ 的相似度矩阵，对角线为正样本，非对角线为负样本。该设计的关键在于**同时保留单模态对比项与跨模态对比项**——消融实验表明，移除单模态对比损失会导致 HUMANISE+ 小批量协议上的平均 mRecall 从 60.00 骤降至 41.77（降幅约 30.4%），而移除跨模态对比损失亦使性能降至 56.07，证明两类对齐对鲁棒的三模态检索均不可或缺。

### 与纯三模态编码器的对比

若直接使用一个三模态编码器（w tri-modal）处理拼接后的三种模态，而不进行显式的高阶分解，其平均 mRecall 低于完整 MonSTeR（见 Table 3）。这表明**显式的拓扑分解**——将三模态关系拆解为节点与边的组合——是实现有效三模态对齐的核心机制，而非简单地增加模型容量。

MonSTeR 的整体 pipeline 围绕一个核心设计原则展开：将文本（t）、运动（m）、场景（s）三种模态视为拓扑三角形，同时建模节点（单模态表示）与边（成对跨模态表示），从而在统一潜在空间中捕捉三者之间的高阶依赖关系。这一设计源自拓扑学中“三向关系必须同时表示单模态与成对跨模态项”的洞察。

**输入与模态编码**

三种输入模态各自通过独立的 Transformer VAE 编码器处理：
- **文本**：经 DistilBERT 获取初始表示后，送入文本 Transformer VAE，生成潜在向量 $v_t$。
- **运动**：$T \times 3 \times 22$ 的运动序列由运动 Transformer VAE 编码为潜在向量 $v_m$。
- **场景**：$N \times 6$ 的彩色点云由场景 Transformer VAE 编码为潜在向量 $v_s$。

每个编码器输出的前两个 token 分别解释为潜在分布的均值和对数方差，用于采样上述单模态潜在向量；其余 token（记为 $\varepsilon_t, \varepsilon_m, \varepsilon_s$）则保留用于跨模态建模。

**跨模态编码器**

三组成对跨模态编码器（ST、MT、MS）接收拼接后的中间 token，生成联合潜在向量：
- ST 编码器：拼接 $\varepsilon_s$ 与 $\varepsilon_t$，输出 $v_{st}$
- MT 编码器：拼接 $\varepsilon_m$ 与 $\varepsilon_t$，输出 $v_{mt}$
- MS 编码器：拼接 $\varepsilon_m$ 与 $\varepsilon_s$，输出 $v_{ms}$

这六个潜在向量（三个单模态 $v_t, v_m, v_s$，三个跨模态 $v_{st}, v_{mt}, v_{ms}$）共同构成统一潜在空间中的完整表示。

**对比对齐与损失计算**

模型通过对比学习将单模态与跨模态嵌入对齐到同一空间。对齐集合定义为：

$$K = \left\{ ( t , s ) , ( m , t ) , ( m , s ) , ( s t , m ) , ( m t , s ) , ( m s , t ) \right\}$$

集合 $K$ 包含三类对齐：
1. **单模态→单模态**：$(t,s), (m,t), (m,s)$，确保各模态的独立表示彼此一致。
2. **跨模态→单模态**：$(st,m), (mt,s), (ms,t)$，使跨模态联合表示能够检索或匹配第三模态。

对于 $K$ 中的每一对 $(i,j)$，计算相似度矩阵 $C_{i,j}$（正样本位于对角线），并施加 InfoNCE 损失。总损失为各项损失的平均：

$$\mathcal { L } _ { \mathrm { t o t } } = \frac { 1 } { | K | } \sum _ { ( i , j ) \in K } \frac { \mathcal { L } _ { \mathrm { N C E } } ( C _ { i , j } ) } { N }$$

**推理流程**

训练完成后，统一潜在空间支持灵活的多任务检索。例如：
- **st2m**：通过 ST 编码器获得场景-文本联合嵌入 $v_{st}$，与运动编码器输出的所有 $v_m$ 计算余弦相似度，排序返回最匹配的运动。
- **ms2t**：通过 MS 编码器获得运动-场景联合嵌入 $v_{ms}$，与文本编码器输出的所有 $v_t$ 计算余弦相似度，返回最匹配的文本描述。

这种设计使得任意模态组合均可作为查询或目标，无需为每个任务单独训练模型。

**关键设计选择与消融验证**

消融实验（Table 3）证实了框架中各组件的必要性：
- 移除所有单模态对比损失（仅保留跨模态对齐）导致 HUMANISE+ 小批量协议平均 mRecall 从 60.00 骤降至 41.77（降幅约 30.4%）。
- 移除所有跨模态对比损失（仅保留单模态对齐）使平均 mRecall 降至 56.07，双模态→单模态检索任务受损尤为严重。
- 采用纯三模态编码器（w tri-modal）未使用显式高阶分解，其性能同样低于完整 MonSTeR，验证了“节点+边”拓扑分解的必要性。

### 单模态编码器

MonSTeR 为三种输入模态分别配备一个基于 Transformer 的变分自编码器（VAE），将原始信号压缩为潜在向量：

- **文本编码器**：以 DistilBERT 作为初始特征提取器，将文本描述转化为 768 维特征，再经 Transformer VAE 编码为潜在向量 $v_t$。
- **运动编码器**：输入为 $T \times 3 \times 22$ 的人体运动序列（$T$ 帧，每帧 3 个根位移分量与 22 个关节旋转分量），经 Transformer VAE 编码为潜在向量 $v_m$。
- **场景编码器**：输入为 $N \times 6$ 的彩色点云（$N$ 个点，每点含 3 维坐标与 3 维颜色），经 Transformer VAE 编码为潜在向量 $v_s$。

每个编码器输出的前两个 token 分别被解释为潜在分布的均值与对数方差，用于采样对应的潜在向量；其余 token（记为 $\varepsilon_t, \varepsilon_m, \varepsilon_s$）则被保留，供后续跨模态编码器使用。

### 跨模态编码器

为显式建模模态之间的高阶交互，MonSTeR 引入三个成对跨模态编码器（ST、MT、MS），分别处理场景-文本、运动-文本、运动-场景的模态对。具体而言，将两个单模态编码器输出的中间 token 进行拼接，送入对应的跨模态 Transformer VAE，生成联合潜在向量：

- ST 编码器：由 $\varepsilon_s$ 与 $\varepsilon_t$ 拼接，生成 $v_{st}$
- MT 编码器：由 $\varepsilon_m$ 与 $\varepsilon_t$ 拼接，生成 $v_{mt}$
- MS 编码器：由 $\varepsilon_m$ 与 $\varepsilon_s$ 拼接，生成 $v_{ms}$

这一设计从拓扑视角出发，将三模态关系 $\{t, s, m\}$ 分解为三个单模态节点与三条成对边，从而在潜在空间中完整表征三者之间的高阶依赖。

### 对比对齐目标

MonSTeR 的核心训练机制是在统一潜在空间中对齐单模态表示与跨模态表示。对比学习的模态对集合 $K$ 定义为：

$$K = \left\{ ( t , s ) , ( m , t ) , ( m , s ) , ( s t , m ) , ( m t , s ) , ( m s , t ) \right\}$$

该集合包含两类对比对：
- **单模态-单模态对**：$(t,s)$、$(m,t)$、$(m,s)$，用于对齐不同模态的单模态表示。
- **跨模态-单模态对**：$(st,m)$、$(mt,s)$、$(ms,t)$，用于将跨模态联合表示与第三模态的单模态表示对齐。

对于 $K$ 中的每一对 $(i,j)$，首先计算相似度矩阵 $C_{i,j}$，其中第 $n$ 行第 $n'$ 列的元素为批次中第 $n$ 个样本的 $i$ 模态嵌入与第 $n'$ 个样本的 $j$ 模态嵌入之间的余弦相似度。对角线上为正样本对（同一数据的不同模态），非对角线为负样本对。随后对每个相似度矩阵施加 InfoNCE 损失，总损失为所有对的平均：

$$\mathcal { L } _ { \mathrm { t o t } } = \frac { 1 } { | K | } \sum _ { ( i , j ) \in K } \frac { \mathcal { L } _ { \mathrm { N C E } } ( C _ { i , j } ) } { N }$$

其中 $N$ 为批次大小，$|K|=6$ 为对比对数量。该损失迫使模型在统一空间中同时保持单模态表示的判别力与跨模态表示的一致性。

### 关键设计约束

作者在构造 $K$ 时有意排除了可能导致模态坍缩的项。例如，不直接将 $(st, mt)$ 等跨模态-跨模态对纳入对比，因为此类对齐可能使模型忽略某一模态的信息，退化为仅依赖部分模态的捷径解。这一约束保证了三个模态在联合表示中的均衡贡献。

## 实验与关键发现

### 核心实验设置

MonSTeR 在两个重新标注的三模态数据集上进行评估：**HUMANISE+** 和 **TRUMANS+**。两者均使用统一的 LLAMA3 流程进行文本重新标注，以保证文本与场景上下文的对齐质量，并消除原始标注中场景信息缺失带来的偏差。评估采用两种检索协议：
- **全量协议（All Protocol）**：在完整测试集中检索，任务难度高，更接近真实应用场景。
- **小批量协议（Small Batches Protocol）**：在随机抽取的小批量样本中检索，降低检索空间，更聚焦于细粒度区分能力。

评价指标为跨检索排名 {1, 2, 3, 5, 10} 的平均 mRecall。所有模型均在相同的数据划分和标注上训练与评估，确保比较的公平性。

### 主实验结果

#### HUMANISE+ 数据集

Table 1 展示了各方法在 HUMANISE+ 上全部检索任务的结果。MonSTeR 在所有涉及场景的任务上均显著超越基线模型：

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2510_03200/figures/004_Table_1.jpg]]
*Table 1: Tasks and protocols’ results on HUMANISE+ [34] test set. Reported metrics are mRecall computed across ranks {1,2,3,5,10}. Greyed-out results are not directly comparable with those in the same column, as they do not leverage scene information*

- **全量协议**：MonSTeR 平均 mRecall 达到 **4.80**，相比最强场景感知基线 **TMR+S**（2.72）提升 **76.5%**。其中，场景+文本→运动（st2m）任务的提升尤为突出，相对最佳场景感知模型提升约 209%（Table 1, part_006）。
- **小批量协议**：MonSTeR 平均 mRecall 达到 **60.00**，比 TMR+S（47.44）提升 **26.5%**。

值得注意的是，在不涉及场景的传统任务（t2m、m2t）上，MonSTeR 仍保持与专用文本-运动基线（TMR、MoPa）相当的性能，说明引入场景模态并未损害原有检索能力。

#### TRUMANS+ 数据集

Table 2 的结果进一步验证了 MonSTeR 的泛化能力：

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2510_03200/figures/005_Table_2.jpg]]
*Table 2: Tasks and protocols’ results on TRUMANS+ [17] test set. Reported metrics are mRecall computed across ranks {1, 2, 3, 5, 10}. Greyed-out results are not directly comparable with those in the same column, as they do not leverage scene information*

- **全量协议**：MonSTeR 平均 mRecall 为 **7.42**，比 TMR+S（5.49）提升 **35.1%**。
- **小批量协议**：MonSTeR 平均 mRecall 为 **47.05**，比最强基线 MoPa+S（42.60）提升 **10.4%**。

TRUMANS+ 上的提升幅度小于 HUMANISE+，这与 TRUMANS+ 场景多样性较低、场景线索对运动检索的约束作用较弱有关。在 t2m 和 m2t 任务上，TMR 甚至略优于 MonSTeR，进一步说明当场景信息价值有限时，专用双模态模型可能更高效——但 MonSTeR 的统一架构并未因此产生明显的负迁移。

### 消融实验

Table 3 和 Table 4 分别报告了 HUMANISE+ 和 TRUMANS+ 上的消融结果，系统验证了 MonSTeR 各组件的贡献。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2510_03200/figures/008_Table_3.jpg]]
*Table 3: Ablation Studies for MonSTeR performed on HUMANISE+ [34]. We report the average mRecall computed across ranks*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2510_03200/figures/009_Table_4.jpg]]
*Table 4: Ablation Studies for MonSTeR performed on TRUMANS+ [17]. We report the average mRecall computed across ranks*

#### 单模态对比损失的关键作用

移除所有单模态对比损失（**MonSTeR w/o single**）后，HUMANISE+ 小批量协议平均 mRecall 从 60.00 骤降至 **41.77**，降幅约 30.4%。这表明单模态表示（$v_t, v_m, v_s$）的对齐对于维持潜在空间的结构至关重要：仅依赖跨模态对齐会导致模态内部表征退化，进而损害所有检索任务的性能。

#### 跨模态对比损失的贡献

移除所有跨模态对比损失（**MonSTeR w/o cross-modal**）后，平均 mRecall 降至 **56.07**。虽然降幅小于移除单模态损失，但双模态→单模态任务（如 st2m、mt2s）的性能显著恶化，验证了跨模态编码器生成的联合潜在向量（$v_{st}, v_{mt}, v_{ms}$）对于处理复合查询不可或缺。

#### 高阶分解的必要性

采用纯三模态编码器（**MonSTeR w tri-modal**）——即不使用成对跨模态分解而直接编码三模态交互——其平均 mRecall 低于完整 MonSTeR。这从实证角度支持了方法设计的核心拓扑直觉：三模态关系 $\{t, s, m\}$ 的完整表示需要同时建模单模态节点和成对跨模态边，直接压缩为单一三模态表示会丢失可分解的高阶依赖信息。

### 定性分析

Figure 4 展示了 st2m 和 ms2t 任务的检索定性结果。在 st2m 任务中，给定场景和文本描述，MonSTeR 能够检索出与场景上下文高度匹配的运动序列；在 ms2t 任务中，模型能准确识别运动与场景的联合语义并匹配正确的文本描述。排序靠前的检索结果与 Ground Truth 高度一致。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2510_03200/figures/006_Figure.jpg]]
*Figure: (a) Walk to the desk near a computer and monitor, passing by a cabinet. (b) Stand up from the sofa chair, which is near the door, a table and a wall. (c) Walk to a chair in front of a laptop, passing by a backpack and a blackboard*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2510_03200/figures/007_Figure_4.jpg]]
*Figure 4: (f) Walk past the wall and extinguisher to the doorframe. Walk to the doorframe, passing by an exit sign. Walk to the door, passing by a table and a cabinet. Figure 4. Qualitative examples for st2m (4c, 4b, 4a) and ms2t (4f, 4e, 4d). First, second, and third retrieved samples are shown. In each pictorial, GT=color (top-left corner) indicates the correct corresponding motion (top row) and text (bottom row)*

Figure 5 通过可控退化实验进一步验证了 MonSTeR 的评估敏感度：随着运动序列被逐步旋转（0 到 $\pi$ 弧度），模型的 FID 指标单调上升、Recall@1 单调下降，表明 MonSTeR 对运动质量的变化具有平滑且敏感的响应能力。

### 用户研究

在运动质量评估的用户研究中，MonSTeR 的检索评分与人类偏好的对齐准确率达到 **66.5%**（Section 4.4），证明模型不仅能执行检索任务，还能有效评估生成运动与场景、文本的三方一致性。这为 MonSTeR 作为运动生成评估器的应用提供了实证支持。

### 失败模式与局限性

1. **场景信息价值不均**：在 TRUMANS+ 等场景多样性较低的数据集上，MonSTeR 的优势收窄，部分传统任务（t2m、m2t）甚至略低于专用双模态模型。场景编码器的引入在此类场景中可能引入冗余信息而非有效约束。
2. **静态场景假设**：当前场景编码器将环境建模为静态点云，无法表示人类动作对环境的动态改变（如移动椅子、开门）。这限制了模型在交互式场景中的应用。
3. **跨模态编码器的数据依赖**：跨模态编码器仅在已对齐的三模态数据上训练，未能利用大量未配对的双模态或单模态数据，限制了模型的泛化潜力和数据效率。

### 运动字幕生成扩展

Table 5 和 Table 6 报告了 MonSTeR 在运动字幕生成任务上的性能。通过将 MonSTeR 的潜在表示与 GPT2 解码器结合，模型在 HUMANISE+ 和 TRUMANS+ 上均优于专用运动字幕模型 mGPT，进一步验证了统一潜在空间在下游生成任务中的迁移能力。

## 定位与知识库关联

### 1. 基线关系与差异化

MonSTeR 的核心差异化在于将**场景上下文**显式纳入人类运动检索与评估的建模框架，这与仅关注文本-运动对齐的现有方法形成根本区别。

**纯文本-运动基线**：**TMR**（Petrovich et al., ICCV 2023）和 **MoPa**（Yu et al., CVPR 2024）仅建模文本与运动两种模态，通过对比学习将二者映射到共享潜在空间。这些方法在 t2m（文本→运动）和 m2t（运动→文本）任务上表现良好，但完全忽略了场景对运动意图的约束——例如“坐下”这一动作在有无椅子时具有截然不同的合理性。

**场景感知扩展基线**：TMR+S 和 MoPa+S 是在上述纯文本-运动模型基础上，通过增加场景编码器得到的朴素三模态扩展。它们能够编码场景信息，但本质上仍只进行单模态表示之间的对齐，缺乏对跨模态高阶交互的显式建模。这导致它们在需要联合理解两种模态以检索第三种模态的任务（如 st2m，即场景+文本→运动）上表现显著弱于 MonSTeR。

**定量差距**：在 HUMANISE+ 数据集的 All 协议下，MonSTeR 的平均 mRecall 达到 4.80，相比最强的场景感知基线 TMR+S（2.72）提升 76.5%；在 Small Batches 协议下，MonSTeR 达到 60.00，相比 TMR+S（47.44）提升 26.5%（Table 1）。在 st2m 这一核心三模态任务上，MonSTeR 相对场景感知基线的提升幅度达到 209%，凸显了高阶交互建模的不可替代性。

### 2. 适用边界与能力范围

**模态覆盖**：MonSTeR 当前专为**文本-运动-场景**三模态设计，场景模态被假定为静态彩色点云。模型支持六种检索任务：三种单模态→单模态（t2m, m2t, t2s 等）和三种跨模态→单模态（st2m, mt2s, ms2t），覆盖了从双模态查询到单模态检索的完整组合空间。

**数据依赖**：模型的跨模态编码器（ST, MT, MS）仅在已对齐的三模态数据上训练，即每个训练样本必须同时包含文本描述、运动序列和场景点云。这限制了模型利用大量未配对单模态或双模态数据的能力，在数据稀缺场景下泛化潜力受限。

**场景假设**：当前框架将场景视为**静态**点云，无法建模人类动作对环境的动态改变（如移动椅子、开门等交互行为）。这意味着 MonSTeR 适用于评估“动作是否适配给定场景”，但不适用于评估“动作如何改变场景”。

### 3. 局限性与失效模式

1. **静态场景假设**：场景编码器以单帧点云为输入，忽略了人类运动过程中可能发生的环境状态变化。当动作涉及物体操作（抓取、推动）或场景布局改变时，模型的一致性评估可能失效。

2. **跨模态编码器的数据效率**：消融实验（Table 3）表明，移除跨模态对比损失后平均 mRecall 从 60.00 降至 56.07，而移除单模态对比损失后骤降至 41.77。这说明单模态表示是跨模态检索的**必要基础**，但也暗示跨模态编码器对对齐数据的依赖较强，在标注稀疏时可能难以充分训练。

3. **场景信息稀疏时的退化**：在 TRUMANS+ 数据集上，MonSTeR 相对基线的提升幅度（All 协议 +35.1%，Small Batches 协议 +10.4%）明显小于 HUMANISE+ 上的提升。分析指出 TRUMANS+ 中的场景线索价值有限，当场景信息本身对任务的区分度不高时，高阶交互建模的边际收益会降低。

4. **纯三模态编码器的次优性**：消融中尝试了使用单一三模态编码器直接建模 {t, m, s} 联合表示（w tri-modal），其平均 mRecall 低于完整 MonSTeR 的拓扑分解方案。这表明将高阶关系**显式分解**为单模态节点与成对跨模态边的组合，比隐式联合编码更有效——但这也意味着框架的扩展需要谨慎设计模态间的分解结构。

### 4. 开放问题

1. **动态场景扩展**：如何将 MonSTeR 的场景编码器从静态点云升级为时序感知的动态场景表示，使其能够编码并利用人类动作对环境状态的改变？这可能需要引入 4D 场景表示或交互图网络。

2. **未配对数据利用**：能否通过自监督或半监督方式，利用大量未配对的双模态数据（如仅有文本-运动或仅有场景-文本）来训练跨模态编码器？这有望显著提升模型的数据效率和泛化能力。

3. **四模态及以上扩展**：当前基于拓扑分解的高阶交互框架——将 N 模态关系分解为单模态节点与成对跨模态边——是否可以自然地扩展到四个或更多模态（例如加入音频、接触力、物体 affordance）？扩展时对比对齐集合 K 的大小将呈组合增长，计算开销与优化难度需要进一步研究。

4. **场景感知的运动评估标准**：MonSTeR 展示了用检索评分评估运动质量的能力，用户研究表明其与人类偏好的对齐准确率达到 66.5%。但这一评估范式的理论边界（如对何种类型的运动错误最敏感）尚未被系统分析，Figure 5 中展示的旋转敏感度实验仅是初步探索。

## 原文 PDF

![[paperPDFs/ICCV_2025/MonSTeR_a_Unified_Model_for_Motion_Scene_Text_Retrieval.pdf]]
