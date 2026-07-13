---
title: "Re-evaluating Continual VQA: Toward Fair and Robust Evaluation for Multimodal Continual Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Re_evaluating_Continual_VQA_Toward_Fair_and_Robust_Evaluation_for_Multimodal_Continual_Learning.pdf
project_link: null
code_link: null
aliases:
- MMDQR
- RECVTFREMCL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 强制实行任务间token级别的不相交答案空间，并引入任务内的训练‑测试答案分布偏移（proposed splits），切除共享答案带来的虚假抗遗忘效应，同时创建鲁棒性检验场景。
primary_logic: 只有切断跨任务答案词汇重叠、引入分布偏移，才能公平测量持续VQA的真实遗忘与泛化能力；基于仅问题回放的匹配与双重蒸馏机制既减少了内存开销，又通过强化跨模态对齐显著提升了鲁棒性与知识保留。
claims:
- 在原始VQA v2上，答案相似性矩阵与准确率矩阵存在强Spearman相关性（SFT corr=0.73, EWC corr=0.69, LwF corr=0.42），表明性能提升大部分来自答案共享而非真正保留。
- 在VQA v3上去除词汇重叠后，模型表现出持续的性能衰减，虚假的抗遗忘现象消失。
- 在PS设置下，SFT与LwF的预测分布高度追随训练分布而非测试集真实分布，显示模型缺乏鲁棒性。
- MaDQ在所有UCo-VQA设定上均取得最高的FAA/CAA和最低的FFM，在PS设定下CAA分别提升4.18%和2.21%。
---

# Re-evaluating Continual VQA: Toward Fair and Robust Evaluation for Multimodal Continual Learning

> [!tip] 核心洞察
> 只有切断跨任务答案词汇重叠、引入分布偏移，才能公平测量持续VQA的真实遗忘与泛化能力；基于仅问题回放的匹配与双重蒸馏机制既减少了内存开销，又通过强化跨模态对齐显著提升了鲁棒性与知识保留。

| 字段 | 内容 |
|------|------|
| 中文题名 | 重新评估持续VQA：迈向多模态持续学习的公平与鲁棒评价 |
| 英文题名 | Re-evaluating Continual VQA: Toward Fair and Robust Evaluation for Multimodal Continual Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gao_Re-evaluating_Continual_VQA_Toward_Fair_and_Robust_Evaluation_for_Multimodal_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | MaDQ (Matching and Distillation with Question replay) |
| Dataset | VQA v3, GQA v2 |

> [!tip] 效果简介
> - VQA v3 (Proposed Splits) 上，CAA (↑) 37.82 vs 32.58 (CLS-ER) (+4.18%)；FFM (↓) 4.54 vs 7.56 (CLS-ER) (-3.02)。
> - GQA v2 (Proposed Splits) 上，CAA (↑) 45.18 vs 39.84 (CLS-ER) (+2.21%* (文中报告+2.21%为鲁棒性/保留提升，此处为CAA绝对提升))；FFM (↓) 9.37 vs 10.91 (CLS-ER, approximate from part analysis) (-1.54)。

## 概要

持续视觉问答（Continual VQA）要求模型在顺序学习新任务时保留过往知识，但现有基准存在两个结构性缺陷，严重扭曲了遗忘测量的公平性。其一，任务间共享答案词汇导致模型依赖答案先验记忆而非真正的视觉语义保留，造成遗忘程度被系统性低估。在原始VQA v2上，答案相似性矩阵与准确率矩阵的Spearman秩相关系数高达0.73（SFT）和0.69（EWC），p < 0.001，表明性能提升大部分来自答案共享的虚假效应。其二，任务内训练与测试答案分布相同，无法评估模型在分布偏移下的鲁棒性，掩盖了知识的脆弱性——在引入分布偏移的PS设置下，SFT与LwF的预测分布高度追随训练分布而非测试集真实分布，揭示模型缺乏真正的泛化能力。

针对上述瓶颈，本文提出**UCo-VQA**基准套件，通过强制实行任务间token级别的不相交答案空间，并引入任务内训练‑测试答案分布偏移，切除共享答案带来的虚假抗遗忘效应，同时创建鲁棒性检验场景。在此基础上，提出**MaDQ**（Matching and Distillation with Question replay）方法，其核心机制包括三项关键设计：仅回放过往问题文本而不存储图像与答案，将内存开销压缩至约0.01 MB/任务；构建答案预测蒸馏与图文匹配蒸馏的双层级蒸馏体系，强化跨模态对齐与知识保留；采用双LoRA架构，以动量适配器提供稳定蒸馏目标。实验表明，MaDQ在所有UCo-VQA设定上均取得最高的累积平均准确率（CAA）和最低的前向遗忘（FFM），在VQA v3 PS设定下CAA较最优基线CLS-ER提升4.18%，FFM降低3.02；在GQA v2 PS设定下CAA提升约2.21%，验证了仅问题回放与双层级蒸馏在公平评价下的有效性。



### 持续VQA的兴起与隐忧

视觉问答（Visual Question Answering, VQA）要求模型理解图像与自然语言问题，并生成准确答案。当VQA模型被部署到动态环境中时，它们需要在不遗忘旧知识的前提下持续学习新概念——这构成了**多模态持续学习**的核心挑战。近年来，研究者将多种持续学习策略引入VQA，包括正则化方法（如**EWC**，Kirkpatrick et al., PNAS 2017）、知识蒸馏（如**LwF**，Li & Hoiem, TPAMI 2018）、参数高效适配（如**Layered-LoRA**，Smith et al., CVPR 2023；**MoE-Adapters**，Yu et al., CVPR 2024）以及经验回放（如**ER**，Rolnick et al., NeurIPS 2019；**CLS-ER**，Arani et al., ICLR 2022）等。然而，这些方法在现有持续VQA基准上的“良好表现”是否真实反映了模型的抗遗忘能力？本文给出了否定的答案。

### 现有基准的双重结构缺陷

通过对现有持续VQA评估体系的深入诊断，本文揭示了两项关键的结构性偏差：

**缺陷一：共享答案词汇导致虚假抗遗忘。** 在广泛使用的VQA v2基准中，不同任务间的答案空间存在大量重叠。当模型在新任务上训练时，它可以依赖先前学到的答案先验（如高频答案词“yes”“no”“red”）来“猜对”旧任务的答案，而无需真正保留视觉语义知识。定量证据表明，在VQA v2上，答案相似性矩阵与持续学习准确率矩阵之间存在强Spearman相关性——SFT的相关系数达0.73，EWC达0.69（p < 0.001），LwF为0.42（p < 0.05）。这种相关性意味着，**性能提升的相当部分来自答案共享的统计捷径，而非真正的知识保留**。当本文重新设计VQA v3数据集，强制实行任务间标记级别的不相交答案空间后，虚假的抗遗忘现象消失，模型表现出持续的性能衰减。

**缺陷二：训练-测试分布一致掩盖知识脆弱性。** 现有基准中，同一任务内的训练集与测试集答案分布高度一致。这使得模型只需拟合训练分布即可在测试中取得高分，而无需具备应对分布偏移的鲁棒性。在本文提出的PS（Proposed Splits）设置下——训练与测试答案分布存在显著偏移——SFT与LwF的预测分布高度追随训练分布而非测试集的真实分布，暴露出模型知识的严重脆弱性。

### UCo-VQA：迈向公平与鲁棒的评估框架

为切除上述偏差，本文构建了**UCo-VQA（Unbiased Continual VQA）基准套件**，其核心设计原则包括：

- **标记级不相交答案空间**：不同任务的答案词汇在标记层面完全隔离，杜绝跨任务答案先验泄露。
- **任务内分布偏移**：通过PS设置引入训练-测试答案分布的不匹配，检验模型在真实部署场景下的鲁棒性。
- **多维度指标**：采用FAA（Forward Average Accuracy）、CAA（Cumulative Average Accuracy）和FFM（Forward Forgetting Measure）全面衡量学习能力、累积保留与遗忘程度。

### 方法动机：高效回放与跨模态对齐

在公平评估框架下，现有方法暴露出两个核心短板：(1) 基于完整三元组回放的方法（如ER、CLS-ER）内存开销巨大，每任务需存储约67.53 MB的图像-问题-答案数据；(2) 仅依赖答案预测蒸馏的方法（如LwF）无法维持跨模态语义对齐，在分布偏移下鲁棒性不足。

这驱动了**MaDQ（Matching and Distillation with Question replay）**的设计：通过**仅回放问题文本**将内存开销压缩至0.01 MB/任务，同时引入**双层级蒸馏**——在答案预测和图文匹配两个层面施加一致性约束——既保留任务知识，又强化视觉-语义的跨模态对齐，从而在公平的UCo-VQA基准上实现鲁棒且抗遗忘的持续VQA。



## 核心方法与创新机理

### 1. 基准缺陷的揭示：从虚假抗遗忘到真实遗忘

现有持续VQA基准存在两个结构性的评估缺陷，导致模型的遗忘程度被严重低估：

**缺陷一：任务间共享答案词汇导致虚假抗遗忘。** 传统VQA v2基准中，不同任务之间共享大量答案词汇（如颜色词、计数词）。当模型在新任务上学习时，只需依赖先前任务中习得的答案先验即可给出看似正确的回答，而无需真正保留跨模态的视觉语义知识。论文通过定量分析证实了这一点：在VQA v2上，任务间答案相似性矩阵与持续学习准确率矩阵之间存在显著的Spearman秩相关性——SFT (corr=0.73, p<0.001)、EWC (corr=0.69, p<0.001)、LwF (corr=0.42, p<0.05)。这一相关性表明，模型在旧任务上的表现提升很大程度上来自答案词汇的跨任务共享，而非真正的知识保留。例如，SFT在Location任务上的准确率呈现剧烈波动（38.44→1.28→34.13→27.08→0.34→0.07→41.58→18.07），这种“遗忘-恢复”的异常模式恰恰暴露了答案先验的干扰效应。

**缺陷二：任务内训练与测试答案分布相同，掩盖知识脆弱性。** 传统基准中，同一任务的训练集和测试集答案分布高度一致，模型只需拟合训练分布即可获得高测试准确率，而无需真正建立鲁棒的跨模态理解。当引入训练-测试分布偏移（Proposed Splits, PS）后，模型预测分布高度追随训练分布而非测试集的真实分布（Figure 2），暴露出知识的本质脆弱性。

### 2. 基准重构：UCo-VQA的因果干预

针对上述缺陷，论文提出了**UCo-VQA (Unbiased Continual VQA)** 基准套件，通过两个关键干预切除虚假信号：

- **Token级不相交答案空间（VQA v3）：** 将VQA v2重新设计为任务间答案词汇完全不相交的VQA v3变体。对于二值问题（如yes/no），为每个任务分配独立的三位八进制编码（如T1使用000/001，T2使用002/003），从根源上杜绝跨任务答案共享。在此设定下，Figure 1(c)中原有的虚假抗遗忘现象消失，模型表现出持续的性能衰减，首次呈现了持续VQA的真实遗忘图景。
- **任务内分布偏移（PS设定）：** 在训练集与测试集之间引入答案分布偏移，强制评估模型在分布外场景下的鲁棒性，而非对训练分布的简单记忆。

Table 1概述了UCo-VQA的完整构成，涵盖SS（标准划分）与PS（分布偏移划分）两种设定，以及共享与不相交两种答案词汇模式，为持续VQA提供了多维度的公平评价框架。

### 3. 方法创新：MaDQ的三大changed slots

在揭示基准缺陷的基础上，论文提出了**MaDQ (Matching and Distillation with Question replay)**，其核心创新体现在三个关键设计维度上，与现有方法形成系统性差异：

| 设计维度 | 现有方法 | MaDQ | 创新本质 |
|---------|---------|------|---------|
| **回放内容** | 完整三元组（图像-问题-答案），如ER、CLS-ER | 仅回放过往问题文本（问题-仅回放） | 将存储成本从67.53 MB/任务降至0.01 MB/任务，同时避免图像与答案的隐私泄露风险 |
| **蒸馏对象** | 仅对答案预测进行蒸馏（如LwF） | 双层级蒸馏：答案预测蒸馏（APD）+ 匹配一致性蒸馏（MCD） | 在保留答案知识的同时，通过图文匹配边界的一致性约束增强跨模态对齐的鲁棒性 |
| **适配器结构** | 单一LoRA或全参数微调 | 双LoRA架构：工作适配器（LoRA-w）+ 动量适配器（LoRA-m） | LoRA-w负责当前任务学习，LoRA-m通过EMA更新提供稳定的蒸馏参考目标，避免灾难性遗忘 |

#### 3.1 问题-仅回放：最小化存储与隐私代价

MaDQ维护一个仅包含历史问题文本的缓冲区$\mathcal{M}$，将其与当前任务图像$\mathcal{X}^t$配对构造伪样本$(x^t, q^i)$。这一设计的关键洞察在于：**跨模态知识保留的核心在于稳定图文语义关联，而非完整三元组的精确记忆。** 问题文本作为跨模态查询的“锚点”，足以触发旧知识的蒸馏约束。

#### 3.2 双层级蒸馏：答案保留与匹配一致性

MaDQ的训练目标由四个层次化组件构成：
$$\mathcal{L} = \underbrace{\mathcal{L}_{\mathrm{TSA}}}_{\mathrm{learning}} + \underbrace{\mathcal{L}_{\mathrm{APD}}}_{\mathrm{retention}} + \underbrace{(\mathcal{L}_{\mathrm{IQM}} + \mathcal{L}_{\mathrm{MCD}})}_{\mathrm{robustness}}$$

- **$\mathcal{L}_{\mathrm{APD}}$（答案预测蒸馏）：** 利用当前图像与历史问题构建伪样本，最小化旧模型与当前模型预测的KL散度，保留答案生成能力。
- **$\mathcal{L}_{\mathrm{IQM}}$（图文匹配损失）：** 通过二分类交叉熵强制模型判断图文是否语义匹配，增强跨模态对齐的基础能力。
- **$\mathcal{L}_{\mathrm{MCD}}$（匹配一致性蒸馏）：** 在图文匹配概率上施加KL散度约束，维持跨模态边界的时序一致性，这是MaDQ鲁棒性提升的核心来源。

消融实验（Table 4）证实了$\mathcal{L}_{\mathrm{IQM}}$的关键作用：在GQA v2 PS设定下，仅使用答案预测蒸馏（MaDQ*）时FFM为12.32，加入$\mathcal{L}_{\mathrm{IQM}}$后降至9.37，遗忘显著减少。更重要的是，将$\mathcal{L}_{\mathrm{IQM}}$集成到ER、CLS-ER等基线方法中（Table 5），在GQA v2上最多可将FFM降低2.33%，验证了该正则化机制的跨方法普适性。

#### 3.3 双LoRA架构：稳定蒸馏与高效适配

MaDQ在视觉-语言骨干网络的所有层（图像编码器$f_\nu$、问题编码器$f_\tau$、答案解码器$f_\omega$的Q/K/V投影、前馈层及token嵌入层）中注入低秩适配器，并维护两个独立分支：

- **LoRA-w（工作适配器）：** 可训练参数，负责当前任务的适应学习。
- **LoRA-m（动量适配器）：** 通过指数移动平均更新（$\bar{A} \leftarrow \alpha \bar{A} + (1-\alpha) A$），为蒸馏提供稳定的参考目标，同时作为推理时的部署模型。

这种双分支设计解决了持续学习中“学习-保留”的根本张力：LoRA-w自由适应新任务，LoRA-m平滑整合历史知识，两者通过蒸馏损失耦合，实现了参数高效的增量学习。

### 4. 创新效果：公平评价下的真实提升

在UCo-VQA的公平评价框架下，MaDQ展现出全面的优势（Table 2）：
- 在VQA v3 PS设定下，CAA达到37.82%，较最强基线CLS-ER（32.58%）提升4.18%；FFM降至4.54，较CLS-ER（7.56）降低3.02。
- 在GQA v2 PS设定下，CAA达到45.18%，FFM降至9.37，均显著优于所有对比方法。
- 在低存储预算下（每任务200样本），MaDQ仅用问题回放即接近ER完整三元组回放的性能（Figure 5），验证了问题-仅回放策略的高效性。

这些提升并非来自对基准偏差的利用，而是在切除答案先验与分布偏移的严格条件下，通过增强跨模态对齐与知识保留机制获得的真实增益。



MaDQ 的整体流程围绕三个核心设计展开：**仅问题回放**、**双层级蒸馏**以及**双LoRA架构**，其训练管线如 Figure 3 所示。模型以当前任务的图像-问题-答案三元组 $(x^t, q^t, a^t)$ 和存储在回放缓冲区 $\mathcal{M}$ 中的过往任务问题作为输入，通过联合优化学习、保留和鲁棒性三个层次的目标，实现跨任务的知识持续积累。

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/004_Figure_3.jpg]]
*Figure 3: Training pipeline of the proposed method with question replay and dual-level distillation. The lower row shows the trainable working adapters for task adaptation, while the upper row depicts the momentum adapters serving as stable references for distillation*

### 模块组成与数据流

系统由以下功能模块串联构成：

- **图像编码器 $f_\nu$**：提取给定图像 $x$ 的视觉特征表示。
- **问题编码器 $f_\tau$**：接收图像特征与问题文本 $q$，执行跨模态融合，生成多模态联合表示。
- **答案解码器 $f_\omega$**：将融合后的多模态表示解码为回答表示。
- **答案分类头 $h_{\text{cls}}$**：基于回答表示输出最终答案预测 $\phi(x, q)$，其形式化定义为：

$$\phi(x, q) = h_{\text{cls}}(f_{\omega}(f_{\tau}(f_{\nu}(x), q)))$$

- **图文匹配头 $h_{\text{IQM}}$**：以多模态联合表示为输入，执行二分类任务——判断图像与问题是否语义匹配，输出匹配概率 $\psi(x, q)$，用于强化跨模态对齐。

### 双LoRA适配器机制

为在持续学习场景下实现参数高效微调，MaDQ 在上述骨干网络的全层（包括 Q/K/V 投影、前馈层和 token 嵌入层）中注入低秩适配器（LoRA），并维护两条独立的 LoRA 分支：

- **工作适配器 LoRA-w**：可训练的低秩矩阵 $(A, B)$，负责当前任务的适应与优化。
- **动量适配器 LoRA-m**：通过指数移动平均（EMA）从 LoRA-w 更新，作为稳定的蒸馏参考模型，同时用于推理。更新规则为：

$$\bar{A} \leftarrow \alpha \bar{A} + (1-\alpha) A, \quad \bar{B} \leftarrow \alpha \bar{B} + (1-\alpha) B$$

### 训练目标层次

总损失函数由四个分量构成，分别对应学习、保留和鲁棒性三个目标：

$$\mathcal{L} = \underbrace{\mathcal{L}_{\mathrm{TSA}}}_{\mathrm{learning}} + \underbrace{\mathcal{L}_{\mathrm{APD}}}_{\mathrm{retention}} + \underbrace{(\mathcal{L}_{\mathrm{IQM}} + \mathcal{L}_{\mathrm{MCD}})}_{\mathrm{robustness}}$$

- **$\mathcal{L}_{\mathrm{TSA}}$（任务特定回答损失）**：当前任务的标准交叉熵损失，驱动模型学习新知识。
- **$\mathcal{L}_{\mathrm{APD}}$（答案预测蒸馏损失）**：利用当前任务图像 $x^t$ 与回放缓冲区 $\mathcal{M}$ 中的历史问题 $q^i$ 构造伪样本，最小化当前模型与旧模型（LoRA-m）在答案预测上的 KL 散度，抑制灾难性遗忘。
- **$\mathcal{L}_{\mathrm{IQM}}$（图文匹配损失）**：二分类交叉熵损失，强制模型区分图文是否语义匹配，增强跨模态对齐的鲁棒性。
- **$\mathcal{L}_{\mathrm{MCD}}$（匹配一致性蒸馏损失）**：在图文匹配概率上施加时序一致性约束，最小化当前模型与旧模型匹配输出的 KL 散度，维持跨模态决策边界的稳定。

### 仅问题回放策略

与传统经验回放（ER）存储完整图像-问题-答案三元组不同，MaDQ 的缓冲区 $\mathcal{M}$ 仅保留过往任务的问题文本。每个任务仅需存储约 0.01 MB 的问题数据，而 ER 等完整回放方法需约 67.53 MB/任务，显著降低了内存开销。训练时，回放问题与当前任务图像配对形成伪样本，配合双层级蒸馏实现高效的知识保留。

> **需注意**：仅问题回放策略在极低存储预算下性能仍有退化，且问题文本的回放可能引发隐私顾虑，论文未提供差分隐私或联邦学习等缓解方案的具体实现。



### 模型整体架构

MaDQ 的基础 VQA 模型由四个串行模块构成：**图像编码器** $f_\nu$ 提取视觉特征，**问题编码器** $f_\tau$ 执行跨模态融合，**答案解码器** $f_\omega$ 生成回答表示，以及**答案分类头** $h_{\text{cls}}$ 输出最终答案预测。给定图像 $x$ 和问题 $q$，预测过程可形式化为：

$$\phi(x, q) = h_{\text{cls}}(f_{\omega}(f_{\tau}(f_{\nu}(x), q))) \tag{1}$$

在此基础上，MaDQ 引入两个关键扩展：**图文匹配头** $h_{\text{IQM}}$ 和**双 LoRA 适配器**架构，分别服务于跨模态对齐增强与高效持续学习。

### 双 LoRA 适配器架构

为实现参数高效的持续学习，MaDQ 在视觉-语言骨干网络的所有层中注入低秩适配器，涵盖图像编码器、问题编码器和答案解码器的 Q/K/V 投影层、前馈层及 token 嵌入层。系统维护两个独立的 LoRA 分支：

- **工作适配器 LoRA-w**：可训练的适配器，负责当前任务的参数更新与适应。
- **动量适配器 LoRA-m**：通过指数移动平均（EMA）从 LoRA-w 更新，作为稳定的蒸馏参考模型，同时用于推理阶段。

动量适配器的更新规则为：

$$\bar{A} \leftarrow \alpha \bar{A} + (1-\alpha) A, \quad \bar{B} \leftarrow \alpha \bar{B} + (1-\alpha) B \tag{8}$$

其中 $A, B$ 为 LoRA-w 的低秩矩阵，$\bar{A}, \bar{B}$ 为 LoRA-m 的对应矩阵，$\alpha$ 控制动量更新的平滑程度。这一设计使 LoRA-m 始终维持一个历史知识的稳定快照，为后续蒸馏提供可靠的教师信号。

### 问题-仅回放策略

MaDQ 采用内存高效的问题-仅回放机制。系统维护一个缓冲区 $\mathcal{M}$，仅存储过往任务的问题文本，不保留图像和答案。在训练当前任务 $t$ 时，将缓冲区中的历史问题 $q^i \in \mathcal{M}$ 与当前任务的图像 $x^t \in \mathcal{X}^t$ 配对，构造伪样本 $(x^t, q^i)$ 用于知识保留训练。该策略使每任务的内存开销仅为约 0.01 MB，远低于完整三元组回放的 67.53 MB/任务。

### 训练目标分解

MaDQ 的总损失函数由学习、保留和鲁棒性三个层次的目标组合而成：

$$\mathcal{L} = \underbrace{\mathcal{L}_{\mathrm{TSA}}}_{\mathrm{learning}} + \underbrace{\mathcal{L}_{\mathrm{APD}}}_{\mathrm{retention}} + \underbrace{(\mathcal{L}_{\mathrm{IQM}} + \mathcal{L}_{\mathrm{MCD}})}_{\mathrm{robustness}} \tag{2}$$

#### 1. 任务特定回答损失（$\mathcal{L}_{\text{TSA}}$）

当前任务的标准监督学习目标，采用交叉熵损失：

$$\mathcal{L}_{\mathrm{TSA}} = \frac{1}{|\mathcal{T}^t|} \sum_{(x^t, q^t, a^t) \in \mathcal{T}^t} \mathcal{L}_{\mathrm{CE}}(\phi^t(x^t, q^t), a^t) \tag{3}$$

其中 $\mathcal{T}^t$ 为当前任务的训练三元组集合，$\phi^t$ 为当前模型（使用 LoRA-w）的预测函数。

#### 2. 答案预测蒸馏损失（$\mathcal{L}_{\text{APD}}$）

利用问题-仅回放构造的伪样本，最小化当前模型与历史模型（LoRA-m）在答案预测上的 KL 散度，以保留旧任务知识：

$$\mathcal{L}_{\mathrm{APD}} = \frac{1}{|\mathcal{X}^t| |\mathcal{M}|} \sum_{x^t \in \mathcal{X}^t, q^i \in \mathcal{M}} \mathcal{L}_{\mathrm{KL}}(\phi^t(x^t, q^i), \phi^{t-1}(x^t, q^i)) \tag{4}$$

其中 $\phi^{t-1}$ 为上一任务结束时的动量模型。该损失强制当前模型在旧问题上维持与历史模型一致的输出分布，从而缓解灾难性遗忘。

#### 3. 图文匹配损失（$\mathcal{L}_{\text{IQM}}$）

为增强跨模态语义对齐，MaDQ 引入图文匹配头 $\psi^t$（即 $h_{\text{IQM}}$），执行二分类任务判断图文是否语义匹配。正样本为当前任务的真实图文对，负样本通过随机打乱图文配对构造：

$$\mathcal{L}_{\mathrm{IQM}} = \frac{1}{|\mathcal{X}^t| |\mathcal{Q}^t \cup \mathcal{M}|} \sum_{x^t \in \mathcal{X}^t, q^j \in \mathcal{Q}^t \cup \mathcal{M}} \mathcal{L}_{\mathrm{CE}}(\psi^t(x^t, q^j), y) \tag{6}$$

其中 $y \in \{0, 1\}$ 表示匹配标签。该损失迫使模型学习细粒度的图文语义对应关系，是提升分布偏移下鲁棒性的关键机制。

#### 4. 匹配一致性蒸馏损失（$\mathcal{L}_{\text{MCD}}$）

在图文匹配概率上施加时序一致性约束，维持跨模态决策边界的稳定：

$$\mathcal{L}_{\mathrm{MCD}} = \frac{1}{|\mathcal{X}^t| |\mathcal{Q}^t \cup \mathcal{M}|} \sum_{x^t \in \mathcal{X}^t, q^j \in \mathcal{Q}^t \cup \mathcal{M}} \mathcal{L}_{\mathrm{KL}}(\psi^t(x^t, q^j), \psi^{t-1}(x^t, q^j)) \tag{7}$$

该损失与 $\mathcal{L}_{\text{APD}}$ 构成双层级蒸馏：答案层级的输出蒸馏保留语义决策能力，匹配层级的表示蒸馏维持跨模态对齐边界。

### 消融验证

消融实验（Table 4）证实了各组件的独立贡献。在 GQA v2 PS 设定下，仅使用答案预测蒸馏的变体 MaDQ* 的遗忘指标 FFM 为 12.32，加入 $\mathcal{L}_{\text{IQM}}$ 后降至 9.37，验证了图文匹配正则化对知识保留的显著增益。进一步将 $\mathcal{L}_{\text{IQM}}$ 集成到 ER、CLS-ER 等基线方法中（Table 5），在 GQA v2 上最多可将 FFM 降低 2.33%，证明该机制的跨方法通用性。

### 补充图表

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/001_Figure_1.jpg]]
*Figure 1: (a) Illustration of the continual learning (CL) evaluation matrix, where each cell represents a metric (e.g., answer similarity or accuracy) between task pairs, and the i-th row shows evaluations on all seen tasks after training up to Ti. (b–c) Visualization of inter-task answer similarity and CL accuracy on VQA v2 and VQA v3 using three representative methods (SFT, EWC, and LwF). Higher inter-task similarity corresponds to smaller forgetting and inflated overall performance, revealing bias in existing benchmarks*

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/002_Figure_2.jpg]]
*Figure 2: Train/test answer distributions and model predictions under the proposed VQA v3 splits (PS). (a) Color and (b) Count tasks. Each column shows the answer distribution in the training set, test set, and model predictions (SFT and LwF). Models largely follow the training answer distribution, indicating limited robustness to distributional shifts*



## 实验与关键发现

### 基准缺陷揭示：共享答案词汇如何制造虚假抗遗忘

现有持续VQA基准的根本缺陷在于任务间共享答案词汇，使模型可以通过记忆答案先验而非真正保留视觉语义来维持性能。论文通过计算任务间答案相似性矩阵与持续学习准确率矩阵的Spearman秩相关性，量化了这一偏差：在原始VQA v2上，**SFT**的相关系数高达0.73（p < 0.001），**EWC**为0.69（p < 0.001），而**LwF**为0.42（p < 0.05）。这种强相关性表明，性能提升的相当部分来自答案重叠带来的虚假效应，而非真正的知识保留。

当答案词汇重叠被切断后（VQA v3），虚假的抗遗忘现象消失，模型表现出持续的性能衰减。以SFT在Location任务上的准确率波动为例：38.44 → 1.28 → 34.13 → 27.08 → 0.34 → 0.07 → 41.58 → 18.07，这种剧烈震荡说明模型在失去答案先验支撑后，知识保留极为脆弱。此外，在PS（Proposed Splits）设置下，SFT与LwF的预测分布高度追随训练分布而非测试集真实分布，进一步揭示了模型在分布偏移下缺乏鲁棒性。

### 主要结果：MaDQ在UCo-VQA上的全面优势

Table 2汇总了各方法在VQA v3和GQA v2上SS与PS设定下的表现。MaDQ在所有设定上均取得最高的FAA/CAA和最低的FFM，具体而言：

- **VQA v3 PS设定**：MaDQ的CAA达到37.82%，相比最强基线**CLS-ER**（32.58%）提升**+4.18%**；FFM降至4.54，较CLS-ER的7.56降低3.02，遗忘程度大幅减轻。
- **GQA v2 PS设定**：MaDQ的CAA为45.18%，较CLS-ER的39.84%提升；FFM为9.37，优于CLS-ER的10.91（下降1.54）。
- 在更简单的SS设定下，MaDQ同样保持领先，验证了方法在不同难度场景下的一致性优势。

值得强调的是，MaDQ的内存开销仅为**0.01 MB/任务**（仅存储问题文本），远低于**ER**等完整回放方法的67.53 MB/任务，实现了高效存储与高性能的兼顾。

### 消融分析：双层级蒸馏的关键贡献

Table 4的消融实验揭示了各损失组件对MaDQ性能的贡献。在GQA v2 PS设定下：

- 仅使用答案预测蒸馏（MaDQ*，即移除$\mathcal{L}_{\mathrm{IQM}}$和$\mathcal{L}_{\mathrm{MCD}}$）时，FFM为12.32；
- 加入$\mathcal{L}_{\mathrm{IQM}}$后，FFM降至9.37，提升显著，表明图文匹配正则化对减轻遗忘有实质作用；
- 完整的双层级蒸馏（$\mathcal{L}_{\mathrm{APD}}$ + $\mathcal{L}_{\mathrm{IQM}}$ + $\mathcal{L}_{\mathrm{MCD}}$）在所有指标上达到最优，验证了答案预测保留与跨模态对齐一致性的协同效应。

进一步地，Table 5展示了将$\mathcal{L}_{\mathrm{IQM}}$集成到其他CL方法中的效果：在GQA v2上，ER、CLS-ER等基线的FFM最多可降低**2.33%**，证明图文匹配正则化具有跨方法的通用有效性，并非MaDQ独享的设计红利。

### 存储效率与模型泛化性

Figure 5展示了内存敏感性分析。在低存储预算下（每任务200样本），MaDQ的CAA仍显著优于同等存储的ER，仅用问题回放即接近ER完整三元组回放的性能水平，验证了问题回放策略的高效性。随着存储预算增加，MaDQ持续保持优势，但性能提升逐渐趋缓，说明问题回放已捕获了大部分必要的跨任务信息。

Table 3将方法迁移至**BLIP2**多模态大语言模型上，在VQA v3 SS设定下验证模型泛化性。MaDQ在更大规模架构上仍保持竞争力，表明双LoRA架构与双层级蒸馏的设计不依赖于特定骨干网络。

### 失败模式与局限性

尽管MaDQ在UCo-VQA上表现优异，仍存在以下局限：

1. **隐私敏感场景的适用性**：方法仍需存储过往问题文本作为回放，在高度隐私敏感的场景下可能不适用。论文指出可通过差分隐私或联邦学习缓解，但未提供实验验证。
2. **低存储预算下的性能退化**：当每任务存储样本极少时，问题回放无法完全替代完整三元组回放，性能仍有明显下降，说明问题文本所承载的跨任务信息存在上限。
3. **任务顺序固定假设**：当前方法假设任务顺序固定，未探讨开放式或噪声环境下的持续学习，实际部署中可能面临任务边界模糊的挑战。
4. **分布偏移的局限性**：PS设定虽引入训练-测试分布偏移，但偏移类型仍限于答案分布层面，未涵盖更复杂的视觉域偏移或问题风格变化。

### 开放问题

- 仅问题回放引发的隐私风险如何通过差分隐私或联邦学习有效缓解，同时保持蒸馏效果？
- UCo-VQA框架能否推广至更复杂的开放域VQA或视频问答，其中答案空间天然重叠且分布偏移更加多样？
- 图文匹配正则化与抗遗忘能力的内在关联是否在更多模态（如语音-视觉）和任务架构上成立，能否上升为持续多模态学习的一般性原则？

### 补充图表

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/005_Table_2.jpg]]
*Table 2: Comparison of CL methods on VQA v3 and GQA v2 under SS and PS settings. MaDQ achieves the best overall performance across both settings, showing consistent gains in FAA and CAA and reduced forgetting, particularly under the more challenging PS setting*

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/009_Table_4.jpg]]
*Table 4: Impact of each loss component in the proposed MaDQ*

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/010_Table_5.jpg]]
*Table 5: Performance improvement from integrating*

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/006_Figure_4.jpg]]
*Figure 4: Comparison of CL methods on the original GQA and the debiased GQA v2 (SS). (Top) FAA and CAA; (Bottom) FFM*

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/007_Figure_5.jpg]]
*Figure 5: Performance comparison of MaDQ and ER under varying memory sizes per task*

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/003_Table_1.jpg]]
*Table 1: Overview of the UCo-VQA Benchmark Suite. ‘SS’ denotes standard splits, and ‘PS’ denotes proposed splits with distributional shifts. Answer vocabularies may share tokens across tasks (shared) or be token-level disjoint*

![[assets/figures/papers/paper_list_l2663_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Re_evaluating_Cont/figures/008_Table_3.jpg]]
*Table 3: Performance comparison on VQA v3 (Standard Splits) using the multi-modal large language model BLIP2 [35]*



## 定位与知识库关联

### 持续VQA基准重构：从“虚假抗遗忘”到公平评价

本节定位的核心问题是：**现有持续VQA基准的系统性缺陷如何导致对方法性能的误判，以及MaDQ在修正后的评价框架下处于何种位置**。

**基准缺陷的因果机制。** 现有持续VQA基准（以VQA v2为代表）存在两个结构性问题，二者共同导致遗忘程度被严重低估：

1. **跨任务答案词汇重叠**：不同任务间共享答案token（如颜色任务和计数任务都可能使用“red”“blue”等词汇），使模型可以通过记忆答案先验而非真正保留视觉语义来维持表面性能。证据来自Spearman秩相关分析——SFT的答案相似性矩阵与准确率矩阵的相关性高达0.73（p<0.001），EWC为0.69（p<0.001），LwF为0.42（p<0.05）。这种强相关性表明，性能提升中相当一部分来自答案共享的“捷径”，而非真正的知识保留。

2. **任务内训练-测试分布一致**：传统划分中训练集与测试集的答案分布高度对齐，模型只需拟合训练分布即可获得高测试精度，无法暴露知识在分布偏移下的脆弱性。

**UCo-VQA的修正策略。** 针对上述缺陷，该工作构建了UCo-VQA基准套件，核心修正包括：
- **VQA v3**：强制实行token级别的不相交答案空间（如二值问题使用任务特定的三位八进制编码），切断跨任务答案共享路径。
- **PS（Proposed Splits）**：在任务内引入训练-测试答案分布偏移，创建鲁棒性检验场景。
- **GQA v2**：对原始GQA进行去偏处理，消除其内在的答案先验偏差。

修正效果立竿见影：在VQA v3上，图1(c)中观察到的“虚假抗遗忘”现象消失，模型表现出持续的性能衰减，与真实遗忘规律一致。在PS设置下，SFT与LwF的预测分布高度追随训练分布而非测试集真实分布（Figure 2），直接证实了传统基准下模型鲁棒性的虚高。

### 方法谱系中的位置：回放策略与蒸馏机制的演化

MaDQ在持续VQA方法谱系中占据一个独特位置——它处于**回放方法**与**正则化/蒸馏方法**的交汇点，并通过设计选择显著区别于现有工作。

**回放策略的谱系。** 经验回放是持续学习中缓解遗忘的主流范式，其演化轨迹反映了“存储效率-隐私-性能”的三元权衡：

| 方法 | 回放内容 | 存储开销 | 关键限制 |
|------|---------|---------|---------|
| **ER** (Rolnick et al., NeurIPS 2019) | 完整（图像-问题-答案）三元组 | 高（~67.53 MB/任务） | 存储与隐私负担重 |
| **CLS-ER** (Arani et al., ICLR 2022) | 双存储体三元组+蒸馏 | 更高 | 复杂度增加 |
| **GAB** (Das et al., WACV 2025) | 生成增强（无数据） | 零存储 | 生成质量依赖 |
| **MaDQ**（本工作） | 仅问题文本 | 极低（~0.01 MB/任务） | 隐私顾虑部分缓解 |

MaDQ的“仅问题回放”策略在谱系中实现了关键跃迁：将存储从完整三元组缩减为仅问题文本，存储开销降低三个数量级，同时通过将回放问题与当前任务图像配对构建伪样本，维持了跨任务知识蒸馏的能力。这一设计使其在低存储预算下（每任务200样本）的CAA仍显著优于同等存储的ER，接近ER完整回放的性能（Figure 5）。

**蒸馏机制的谱系。** 在无回放或轻量回放的正则化方法中，知识蒸馏是保留旧任务知识的核心手段：

- **LwF** (Li & Hoiem, TPAMI 2018)：仅对答案预测进行蒸馏，缺乏对跨模态对齐的显式约束。
- **EWC** (Kirkpatrick et al., PNAS 2017)：通过参数重要性加权正则化，无蒸馏机制。
- **ZAF** (Gao et al., NeurIPS 2024)：稳定零样本预测，不依赖回放。
- **MaDQ**：引入**双层级蒸馏**——同时蒸馏答案预测（L_APD）和图文匹配一致性（L_MCD），后者通过匹配头h_IQM的二分类输出施加跨模态边界约束。

消融实验揭示了这一设计的必要性：仅使用答案预测蒸馏（MaDQ*）时，GQA v2 PS的FFM为12.32；加入L_IQM后降至9.37（Table 4），验证了图文匹配蒸馏对鲁棒性保留的独立贡献。更关键的是，将L_IQM集成到ER、CLS-ER等基线方法中，在GQA v2上最多可将FFM降低2.33%（Table 5），证明该机制具有跨方法泛化性。

**参数高效适配的谱系。** MaDQ的Dual-LoRA架构在参数高效持续学习谱系中引入了一种新的“工作-动量”双分支范式：

- **Layered-LoRA** (Smith et al., CVPR 2023) 和 **MoE-Adapters** (Yu et al., CVPR 2024)：采用单一适配器或无回放参数隔离，缺乏稳定的蒸馏参考。
- **MaDQ**：维护可训练的LoRA-w（工作适配器）和通过EMA更新的LoRA-m（动量适配器），后者在蒸馏中提供稳定的旧模型参考，推理时也可使用。LoRA适配器被注入图像编码器、问题编码器和答案解码器的所有层（包括Q/K/V投影、前馈层和token嵌入层），确保全面的任务适应能力。

### 适用边界与局限

**适用场景。** MaDQ的设计使其特别适合以下场景：
- **存储受限**的持续VQA部署（如边缘设备），仅需0.01 MB/任务的文本存储。
- **任务序列固定**的离线持续学习，假设任务边界明确且顺序已知。
- **封闭答案词汇**的VQA任务，答案空间可预先定义。

**已知局限。**

1. **隐私不完全保障**：虽然仅回放问题文本大幅降低了隐私风险，但问题本身仍可能包含敏感信息（如医学VQA中的症状描述）。论文明确指出“问题回放可能引发隐私顾虑，需在开放或嘈杂场景进一步研究”。

2. **任务顺序假设**：方法假设任务顺序固定，未探讨开放式或噪声环境下的持续学习。在任务边界模糊或数据流随机的场景中，双LoRA架构的任务切换机制需要额外设计。

3. **低存储预算下的性能退化**：尽管仅问题回放在内存效率上表现优异，但在极低存储预算下性能仍有退化，无法完全替代完整三元组回放的知识保留能力。Figure 5显示，当每任务存储样本降至极低时，MaDQ与ER的差距会扩大。

4. **模型架构依赖**：方法在BLIP骨干上验证，虽在BLIP2上进行了扩展实验（Table 3），但对其他视觉语言架构（如LLaVA、Flamingo）的泛化性仍需验证。

### 开放问题

1. **隐私-性能权衡的深化**：仅问题回放引发的隐私风险如何通过差分隐私或联邦学习进一步缓解？能否设计“无文本存储”的蒸馏机制（如通过合成问题生成）？

2. **框架的跨域推广**：UCo-VQA的“不相交答案空间+分布偏移”评价框架能否推广至更复杂的开放域VQA、视频问答或多轮对话？开放域场景中答案空间的动态性对框架设计提出新挑战。

3. **图文匹配正则化的内在机理**：L_IQM对鲁棒性的提升是否源于更强的跨模态对齐，还是仅通过增加优化约束间接稳定了表示空间？这一机制在更多模态组合（如视频-文本、音频-文本）和任务架构上是否普遍成立？

4. **动态任务序列**：在任务边界未知或数据流包含噪声的开放环境中，双LoRA架构如何自适应地决定何时创建新适配器、何时复用旧适配器？这需要引入任务边界检测或持续聚类机制。

5. **与大规模多模态模型的整合**：随着BLIP2、LLaVA等MLLM的兴起，持续VQA的范式可能从“分类头微调”转向“指令微调”。MaDQ的仅问题回放和双层级蒸馏策略在这种范式下是否仍然有效，需要重新审视。



## 原文 PDF

![[paperPDFs/CVPR_2026/Re_evaluating_Continual_VQA_Toward_Fair_and_Robust_Evaluation_for_Multimodal_Continual_Learning.pdf]]
