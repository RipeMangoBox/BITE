---
title: "DK-DDIL: Adaptive Knowledge Retention for Dynamic Domain-Incremental Learning in Medical Imaging"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DK_DDIL_Adaptive_Knowledge_Retention_for_Dynamic_Domain_Incremental_Learning_in_Medical_Imaging.pdf
project_link: null
code_link: null
aliases:
- DD
- DK-DDIL
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过动态调整LoRA适配器的秩（DAM），根据域复杂性灵活分配模型容量，同时利用选择性适配器融合（MKI）和原型级对比学习（DCL）巩固跨域知识，从而稳定模型可塑性与稳定性平衡。
primary_logic: 将低秩自适应的动态秩选择与参数级融合及原型级对比精炼相结合，形成统一的域感知适配框架，既能根据不同域的数据规模灵活扩展容量，又能在无回放条件下保留和精炼历史知识。
claims:
- DAM adaptively regulates LoRA ranks via learnable masks, scaling factors, and sparsity regularization.
- DK-DDIL consistently outperforms state-of-the-art DIL approaches on Skin Pathology Diagnosis, Cyst-X 3D MRI, and OfficeHome.
- MKI and DCL jointly mitigate feature drift and catastrophic forgetting, evidenced by superior final accuracy AT on all benchmarks.
- Skin Pathology Diagnosis 上 A (平均准确率) = 77.03 ± 0.52
---

# DK-DDIL: Adaptive Knowledge Retention for Dynamic Domain-Incremental Learning in Medical Imaging

> [!tip] 核心洞察
> 将低秩自适应的动态秩选择与参数级融合及原型级对比精炼相结合，形成统一的域感知适配框架，既能根据不同域的数据规模灵活扩展容量，又能在无回放条件下保留和精炼历史知识。

| 字段 | 内容 |
|------|------|
| 中文题名 | DK-DDIL：面向医学影像动态域增量学习的自适应知识保留 |
| 英文题名 | DK-DDIL: Adaptive Knowledge Retention for Dynamic Domain-Incremental Learning in Medical Imaging |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ma_DK-DDIL_Adaptive_Knowledge_Retention_for_Dynamic_Domain-Incremental_Learning_in_Medical_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | DK-DDIL |
| Dataset | Skin Pathology Diagnosis, Cyst-X, OfficeHome, Overall |

> [!tip] 效果简介
> - Skin Pathology Diagnosis 上，A (平均准确率) 77.03 ± 0.52 vs 74.79 ± 0.10 (RanPAC) (+2.24)；AT (最终准确率) 71.52 ± 1.04 vs 66.89 ± 0.09 (RanPAC) (+4.63)。
> - Cyst-X 上，A 53.34 (均值) vs 52.56 ± 1.39 (RanPAC) (+0.78)；AT 51.08 (均值) vs 48.20 ± 4.14 (RanPAC) (+2.88)。
> - OfficeHome 上，A 84.35 ± 0.30 vs 82.22 ± 0.09 (RanPAC) (+2.13)。

## 概述

**问题瓶颈**：真实临床场景中的域增量学习（DIL）面临双重挑战——标签空间随时间动态演变（旧类别延续的同时新类别不断涌现），且不同域的数据规模与类别构成高度异构。现有方法通常假设固定的标签空间，并依赖静态的模型容量分配与独立的域适配器训练，难以在无历史数据回放的约束下平衡可塑性与稳定性，导致灾难性遗忘和跨域泛化能力不足。

**核心洞察**：DK-DDIL 提出了一种统一的域感知适配框架，将低秩自适应（LoRA）的动态秩选择与参数级融合及原型级对比精炼相结合。其关键思路是：让模型根据每个域的复杂度和数据规模，自适应地决定“学多少”（容量分配），同时通过选择性知识继承与特征空间对比约束，在无排练条件下保留并精炼历史知识。

**方法定位**：DK-DDIL 属于适配器基（adapter-based）的持续学习方法，但区别于固定秩 LoRA 或离散秩切换的现有方案。其核心创新在于两个协同模块——**动态适配模块（DAM）** 通过可学习的秩分数与稀疏正则化实现细粒度的连续秩调节；**知识继承与精炼机制（KIR）** 则通过参数融合（MKI）与域对比学习（DCL）在参数空间和特征空间同时维护跨域一致性。分类器采用基于原型的记忆库，以余弦相似度进行增量推理，天然支持动态标签扩展。

**主要结果**：在皮肤病理诊断、Cyst-X 3D MRI 和 OfficeHome 三个互补基准上，DK-DDIL 在平均准确率（A）和最终准确率（AT）上均一致优于现有最先进方法。以皮肤病理诊断为例，AT 达到 71.52%，较最强基线 RanPAC 提升 4.63 个百分点；在仅使用 0.26% 可训练参数的情况下，实现了显著优于参数规模更大的适配器方法的性能，验证了动态容量分配与知识整合策略的有效性。

## 背景与动机

### 医学影像连续学习的现实挑战

持续学习（Continual Learning）旨在使模型在顺序到达的数据流中逐步积累知识，而不会灾难性地遗忘先前学到的信息。在医学影像分析领域，这一需求尤为迫切：临床数据并非一次性静态收集，而是随着时间推移、设备更新、采集协议变化和疾病谱演化而持续涌现。然而，现有的域增量学习（Domain-Incremental Learning, DIL）方法在设计上存在两个根本性假设，使其难以直接部署于真实临床场景。

**第一，固定标签空间的假设。** 传统 DIL 设定中，所有域共享相同的类别集合，仅数据分布发生变化。但在临床实践中，新的疾病类别会随时间不断出现——例如皮肤病理诊断中，早期数据集可能仅包含黑色素瘤和痣，而后期数据集中会引入光化性角化病（AK）、鳞状细胞癌（SCC）等新类别。这种**标签空间的动态演化**（$|\mathcal V_t \cup \mathcal V_{t-1}| \geq |\mathcal V_{t-1}|$，且 $\mathcal V_{t-1} \cap \mathcal V_t \neq \emptyset$）要求模型既能保留旧类别知识，又能无缝扩展对新类别的判别能力。

**第二，有限域异质性的假设。** 现有方法通常假定域间差异是可预测且有限的，但真实临床数据中的域偏移（domain shift）由多种因素复合而成：不同医疗机构的成像设备参数、操作者差异、患者人口统计学特征、染色协议变化等，导致域间分布高度异构。Figure 2 所展示的皮肤病理诊断数据集即典型例证——七个时序域在样本量和类别构成上均存在显著差异，部分域仅有数十例样本，而另一些域包含数千例，且新类别（如 AK、SCC、MAL OTH）在后续域中才首次出现。

### 现有方法的瓶颈

当前主流的 DIL 方法可大致归为三类，但各类方法在面对上述动态域增量学习场景时均存在结构性不足：

- **基于提示（Prompt-based）的方法**，如 **L2P**（Wang et al., CVPR 2022）、**DualPrompt**（Wang et al., ECCV 2022）和 **CODA-Prompt**（Smith et al., CVPR 2023），通过维护可学习的提示池来适应不同域。然而，提示池的大小通常是固定的，无法根据域复杂性灵活扩展容量；当域间差异剧烈时，固定容量的提示池难以同时覆盖所有域的特征空间。

- **基于适配器（Adapter-based）的方法**，如 **RanPAC**（McDonnell et al., NeurIPS 2023）、**EASE**（Zhou et al., CVPR 2024）和 **CL-LoRA**（He et al., CVPR 2025），通过在预训练骨干中插入轻量级模块实现域适应。但这些方法普遍采用固定秩（如 $r=4$）的低秩适配器（LoRA），缺乏对域复杂性的自适应感知——简单域可能浪费容量，复杂域则可能容量不足。此外，各域适配器通常独立训练，缺乏有效的跨域知识整合机制。

- **基于剪枝（Pruning-based）的方法**，如 **GC2**（Bayasi et al., TMI 2024），通过参数稀疏化来保留关键权重，但在动态标签扩展场景下，剪枝策略难以与新类别学习协同优化。

这些方法的共同瓶颈在于：**缺乏自适应的模型容量分配机制**和**跨域知识整合策略**，导致在域分布高度异构且标签空间动态变化的场景下，模型的可塑性（学习新知识）与稳定性（保留旧知识）之间难以取得平衡。

### 本文的核心动机与洞察

DK-DDIL 的核心洞察在于：**将低秩自适应的动态秩选择与参数级融合及原型级对比精炼相结合，形成统一的域感知适配框架。** 具体而言：

1. **动态容量分配**：通过可学习的秩掩码和稀疏正则化，使模型能够根据每个域的数据规模和复杂性，自动调节 LoRA 适配器的有效秩，实现“按需分配”的容量扩展，而非一刀切地使用固定秩。

2. **参数级知识继承**：在训练新域时，通过余弦退火调度选择性融合当前域与历史域的适配器参数（仅融合 B 矩阵），使模型在保留域不变子空间结构的同时，逐步聚焦于新域的特异特征。

3. **原型级对比精炼**：在特征空间施加多粒度对比约束——正对齐损失缓解原型漂移、域内负样本分离增强类间判别、跨域负样本抑制防止新旧类别混淆、类内紧凑性损失强化特征内聚——从而在无回放（rehearsal-free）条件下巩固跨域知识。

这一设计直接回应了动态域增量学习的核心因果机制：通过 DAM 的连续秩调节与 KIR 的参数-原型双重巩固，稳定了模型可塑性与稳定性的平衡点，使模型在标签空间动态扩展和域分布高度异构的双重挑战下，仍能有效抑制灾难性遗忘。

## 核心创新

DK-DDIL 的核心创新在于将**动态秩自适应**与**参数-原型双级知识精炼**统一为端到端的无回放持续学习框架，从而突破现有域增量学习（DIL）方法在标签空间动态演变和域分布高度异构场景下的瓶颈。其关键创新体现在三个 **changed slots** 上：

### 1. 从固定秩到连续可学习的动态秩调节（DAM）

现有基于 LoRA 的持续学习方法（如 **CL-LoRA** (He et al., CVPR 2025)、**EASE** (Zhou et al., CVPR 2024)）通常采用固定秩（如 $r=4$）或域级别离散切换，无法根据域的统计特性（样本量、类别数、分布偏移程度）灵活分配模型容量。

DK-DDIL 提出的 **Dynamic Adaptation Module (DAM)** 将秩选择转化为连续优化问题：为每个 LoRA 适配器维护一个可学习的秩分数向量 $\mathbf{s} \in \mathbb{R}^{r_{\max}}$，通过温度缩放 sigmoid 生成软掩码 $\tilde{m}_i = \sigma(s_i)$，并利用直通估计器（STE）将其二值化为硬掩码 $m_i \in \{0,1\}$，同时保持梯度可微：

$$m_i = \mathbb{I}[\tilde{m}_i > \tau] + (\tilde{m}_i - \operatorname{stopgrad}(\tilde{m}_i))$$

有效秩 $r_{\text{eff}} = \sum_i m_i$ 随域自适应变化，配合动态缩放系数 $\alpha_t = r_{\max} / r_{\text{eff}}$ 调节残差强度，并施加稀疏正则化 $\mathcal{L}_{\text{reg}} = \lambda_{\text{reg}} \cdot \frac{1}{r_{\max}} \sum_i \sigma(s_i)$ 鼓励仅激活最必要的秩成分。这一设计使模型在简单域上自动收缩容量以防止过拟合，在复杂域上扩展容量以增强可塑性，实现了**域感知的容量缩放**。

### 2. 从独立适配器到选择性参数级知识继承（MKI）

传统适配器方法（如 **RanPAC** (McDonnell et al., NeurIPS 2023)、**SimpleCIL** (Zhou et al., IJCV 2025)）各域适配器独立训练，无跨域交互，导致历史知识随域递增而逐渐遗忘。

DK-DDIL 的 **Model Fusion based Knowledge Inheritance (MKI)** 在训练每个新域时，通过余弦退火调度系数 $\alpha_e$ 将当前域 DAM 的 B 矩阵与历史域 B 矩阵的均值进行选择性融合：

$$B^{(t)} \leftarrow \alpha_e B^{(t)} + \frac{(1 - \alpha_e)}{t-1} \sum_{k=1}^{t-1} B^{(k)}$$

$$\alpha_e = \alpha_{\text{final}} + (\alpha_{\text{init}} - \alpha_{\text{final}}) \cdot \frac{1 + \cos(\pi e / E)}{2}$$

训练初期 $\alpha_e$ 较大，偏重知识继承以稳定参数空间；后期 $\alpha_e$ 衰减，逐步释放域特异学习能力。仅融合 B 矩阵（投影矩阵）而非 A 矩阵的策略保留了域不变子空间结构，避免对输入变换的干扰。

### 3. 从标准分类器到原型级对比精炼（DCL）

现有方法多采用标准线性分类器（softmax），在动态标签空间下难以有效分离新旧类别特征，尤其容易产生跨域特征混淆。

DK-DDIL 构建了**原型记忆库**，利用余弦相似度进行增量最近邻分类，并引入 **Domain Contrastive Learning (DCL)** 从四个维度精炼特征空间：

- **正对齐损失** $\mathcal{L}_{\text{pos}}$：鼓励特征与当前域原型对齐，缓解原型漂移；
- **域内对比分离损失** $\mathcal{L}_{\text{neg-intra}}$：原型级 InfoNCE，增强域内类间分离；
- **跨域负样本抑制损失** $\mathcal{L}_{\text{neg-cross}}$：显式惩罚新域特征与语义无关历史原型的错误关联；
- **类内紧凑性损失** $\mathcal{L}_{\text{intra}}$：强化同批次同类样本的特征内聚性。

DCL 通过课程加权系数 $s/S_t$ 随域内观测增加逐渐增强负对比强度，与 MKI 形成互补——MKI 在参数层面巩固域不变知识，DCL 在特征层面抑制跨域混淆。

**证据强度**：消融实验（Figure 3a）表明，移除 DAM 和 KIR 仅微调分类头（FT）导致性能急剧下降，证实了自适应适配器与知识整合的不可或缺性。主实验（Table 1）显示 DK-DDIL 在 Skin Pathology Diagnosis、Cyst-X 3D MRI 和 OfficeHome 三个基准上的最终准确率 $A_T$ 分别达到 71.52%、51.08% 和 86.29%，较最强基线 RanPAC 提升 +4.63%、+2.88% 和 +1.59%，同时仅使用 0.26% 的可训练参数，验证了创新的有效性。

## 整体框架

DK-DDIL 构建了一个**无回放（rehearsal-free）的动态域增量学习框架**，其核心瓶颈在于真实临床场景中标签空间随时间动态演变、域分布高度异构，而现有方法依赖固定标签空间且缺乏自适应的容量分配与跨域知识整合机制，导致灾难性遗忘与泛化退化。该框架通过两个协同模块——**动态适配模块（Dynamic Adaptation Module, DAM）**和**知识继承与精炼模块（Knowledge Inheritance and Refinement, KIR）**——在冻结的 ViT-B/16 骨干上实现域感知的自适应容量扩展与跨域一致性保持，整体结构如图 Figure 1 所示。

![[assets/figures/papers/paper_list_l2119_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_DK_DDIL_Adaptive_Kn/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed DK-DDIL framework. Given sequential domains with evolving label spaces, DK-DDIL enables rehearsal-free continual adaptation through two key components. (1) The Dynamic Adaptation Module (DAM) adaptively adjusts the low-rank capacity of LoRA-based adapters via learnable rank regulation, allowing domain-aware capacity scaling without modifying pretrained weights. (2) The Knowledge Inheritance and Refinement (KIR) mechanism preserves cross-domain consistency through model fusion based knowledge inheritance (MKI) and domain contrastive learning (DCL), which jointly mitigate catastrophic forgetting and enhance inter-domain discriminability*

### 输入输出与数据流约束

框架接收按时间顺序到达的域序列 $\{\mathcal{D}_1, \mathcal{D}_2, \dots, \mathcal{D}_T\}$，每个域 $\mathcal{D}_t$ 包含图像样本与对应的标签集 $\mathcal{V}_t$。与经典域增量学习不同，DK-DDIL 显式建模了两个关键约束：

- **动态标签空间**：$\mathcal{V}_{t-1} \cap \mathcal{V}_t \neq \emptyset$ 且 $|\mathcal{V}_t \cup \mathcal{V}_{t-1}| \geq |\mathcal{V}_{t-1}|$，即已知类别延续的同时新类别随时间涌现；
- **无回放约束**：$\mathcal{D}_i \cap \mathcal{D}_j = \emptyset,\ \forall i \neq j$，历史域数据不可复访。

对于当前域 $\mathcal{D}_t$ 的输入图像 $\mathbf{x}$，冻结的 ViT-B/16 骨干提取特征 $\mathbf{f}_\theta(\mathbf{x})$，最终通过**原型记忆库**中以余弦相似度为基础的最近邻分类器输出预测 $\hat{y} = \arg\max_{c \in \mathcal{V}_{1:t}} \cos(\mathbf{f}_\theta(\mathbf{x}), \mathbf{p}_c)$，其中原型 $\mathbf{p}_c$ 跨域累积更新，天然支持标签空间的动态扩展。

### 核心模块关系

框架的因果调节旋钮在于**将低秩自适应的动态秩选择与参数级融合及原型级对比精炼相结合**，形成统一的域感知适配体系：

1. **DAM（动态适配模块）**：插入 ViT 自注意力和投影（Proj.）层的线性投影中，通过可学习秩分数向量 $\mathbf{s} \in \mathbb{R}^{r_{\max}}$、温度缩放 sigmoid 与直通估计器（STE）实现每域细粒度的动态秩调节，并施加稀疏正则化 $\mathcal{L}_{\text{reg}}$ 以鼓励仅激活最必要的秩成分。动态缩放系数 $\alpha_t = r_{\max} / \sum_i m_i$ 根据有效秩自动平衡预训练知识与域适应参数，使模型容量随域复杂度灵活伸缩。

2. **KIR（知识继承与精炼模块）**：包含两个子组件——
   - **MKI（基于模型融合的知识继承）**：通过余弦退火调度 $\alpha_e$ 选择性融合当前域与历史域 DAM 的 B 矩阵，训练初期偏重知识继承，后期逐渐转向域特异学习，实现参数级跨域一致性；
   - **DCL（域对比学习）**：在特征空间施加原型级对比损失，包括正对齐 $\mathcal{L}_{\text{pos}}$、域内负样本分离 $\mathcal{L}_{\text{neg-intra}}$、跨域负样本抑制 $\mathcal{L}_{\text{neg-cross}}$ 和类内紧凑性 $\mathcal{L}_{\text{intra}}$，并以课程加权策略组合，随域内观测增加逐渐增强负对比强度。

最终训练目标联合交叉熵损失、秩正则化与 DCL 损失：$\mathcal{L} = \mathcal{L}_{\text{CE}} + \mathcal{L}_{\text{reg}} + \mathcal{L}_{\text{DCL}}$。

### 关键证据与效能

实验表明，该框架在 Skin Pathology Diagnosis（7 个序贯域）、Cyst-X 3D MRI 和 OfficeHome 三个互补基准上均一致超越现有最优 DIL 方法。以 Skin Pathology Diagnosis 为例，DK-DDIL 的平均准确率 A 达到 77.03%，最终准确率 AT 达到 71.52%，分别较最强基线 RanPAC（McDonnell et al., NeurIPS 2023）高出 +2.24 和 +4.63 个百分点，同时可训练参数仅占 0.26%，显著低于多数适配器方法。消融实验进一步证实：移除 DAM 和 KIR 仅微调分类头会导致性能急剧下降，验证了自适应适配器与知识整合的不可或缺性。

## 核心模块与公式推导

### 3.1 动态域增量学习形式化

DK-DDIL 面向的是真实临床场景中标签空间动态变化且域分布高度异构的挑战。给定序列域 $\mathcal{D}_1, \mathcal{D}_2, \dots, \mathcal{D}_T$，每个域 $\mathcal{D}_t = \{(\mathbf{x}_i, y_i)\}_{i=1}^{N_t}$ 的标签空间 $\mathcal{V}_t$ 满足动态演化条件：

$$\mathcal{V}_{t-1} \cap \mathcal{V}_t \neq \emptyset, \quad |\mathcal{V}_t \cup \mathcal{V}_{t-1}| \geq |\mathcal{V}_{t-1}|$$

这意味着已知类别得以延续的同时，新类别随时间不断涌现。此外，方法受排练无关约束（rehearsal-free），历史域数据不可复访：

$$\mathcal{D}_i \cap \mathcal{D}_j = \emptyset, \quad \forall i \neq j$$

在此约束下，核心瓶颈在于：如何在无回放条件下，既为每个域灵活分配模型容量，又有效保留和精炼跨域知识，从而稳定模型的可塑性与稳定性平衡。

### 3.2 动态适配模块（DAM）

DAM 是 DK-DDIL 实现域感知容量缩放的核心机制。它在冻结的 ViT 骨干的自注意力和线性投影（Proj.）层中插入低秩适配器（LoRA），通过可学习的秩分数向量动态调节每个适配器的有效秩。

**低秩适配器基础形式**。对于预训练权重矩阵 $W \in \mathbb{R}^{d \times k}$，DAM 引入可学习残差分支：

$$W' = W + \Delta W, \quad \Delta W = AB$$

其中 $A \in \mathbb{R}^{d \times r_{\max}}$、$B \in \mathbb{R}^{r_{\max} \times k}$ 为低秩矩阵，$r_{\max}$ 为预设的最大秩。

**动态秩选择机制**。DAM 维护一个可学习秩分数向量 $\mathbf{s} \in \mathbb{R}^{r_{\max}}$，通过温度缩放 sigmoid 与直通估计器（STE）生成二元掩码，实现离散秩选择的同时保持端到端可微：

$$\tilde{m}_i = \sigma(s_i), \quad m_i = \mathbb{I}[\tilde{m}_i > \tau] + (\tilde{m}_i - \operatorname{stopgrad}(\tilde{m}_i))$$

其中 $\tau$ 为阈值，$\mathbb{I}[\cdot]$ 为指示函数，$\operatorname{stopgrad}(\cdot)$ 阻断梯度传播。有效秩由激活的掩码数量决定：$r_{\text{eff}} = \sum_i m_i$。

**动态缩放系数**。为平衡预训练知识与域适应参数，DAM 根据有效秩动态调节适配器强度：

$$\alpha_t = \frac{r_{\max}}{\sum_i m_i}$$

当有效秩较低时，缩放系数增大以强化适配；当有效秩较高时，缩放系数减小以保留预训练特征。

**秩稀疏正则化**。为鼓励模型仅激活最必要的秩成分，引入稀疏正则化损失：

$$\mathcal{L}_{\text{reg}} = \lambda_{\text{reg}} \cdot \frac{1}{r_{\max}} \sum_{i=1}^{r_{\max}} \sigma(s_i)$$

该损失通过惩罚所有秩分数的 sigmoid 均值，推动模型学习稀疏的秩分配，从而根据域复杂性灵活控制容量。

### 3.3 知识继承与精炼模块（KIR）

KIR 由两个互补的子模块构成：基于模型融合的知识继承（MKI）和域对比学习（DCL），分别在参数空间和特征空间巩固跨域知识。

#### 3.3.1 基于模型融合的知识继承（MKI）

MKI 通过选择性融合当前域 DAM 与历史域 DAM 的低秩投影矩阵 $B$，实现参数级知识继承。核心设计包括：

**余弦退火融合调度**。融合系数 $\alpha_e$ 随训练 epoch 按余弦退火衰减，训练初期偏重知识继承，后期逐渐转向域特异学习：

$$\alpha_e = \alpha_{\text{final}} + (\alpha_{\text{init}} - \alpha_{\text{final}}) \cdot \frac{1 + \cos(\pi e / E)}{2}$$

其中 $\alpha_{\text{init}}$ 和 $\alpha_{\text{final}}$ 分别为初始和最终融合强度，$E$ 为总训练轮数。

**选择性参数融合（仅 B 矩阵）**。MKI 仅融合 $B$ 矩阵以保留域不变子空间结构，避免对 $A$ 矩阵的干扰：

$$B^{(t)} \leftarrow \alpha_e B^{(t)} + \frac{(1 - \alpha_e)}{t-1} \sum_{k=1}^{t-1} B^{(k)}$$

该设计的关键洞察在于：$B$ 矩阵编码了从低秩空间到输出空间的投影方向，融合历史 $B$ 矩阵有助于维持跨域一致的子空间结构，而 $A$ 矩阵保留域特异信息。

#### 3.3.2 域对比学习（DCL）

DCL 在特征空间施加原型级别的多目标对比约束，精炼跨域特征表示。其总体目标为：

$$\mathcal{L}_{\text{DCL}} = \mathcal{L}_{\text{pos}} + \frac{s}{S_t} (\mathcal{L}_{\text{neg-intra}} + \mathcal{L}_{\text{neg-cross}}) + \mathcal{L}_{\text{intra}}$$

其中 $s/S_t$ 为课程加权系数，随域内观测增加逐渐增强负对比强度。

**正对齐损失**。鼓励当前域样本特征与其对应原型对齐，缓解原型漂移：

$$\mathcal{L}_{\text{pos}} = \frac{1}{\mathbb{B}} \sum_{i=1}^{\mathbb{B}} [1 - \cos(\mathbf{f}_i, \mathbf{p}_{y_i}^{(t)})]$$

**域内对比分离损失**。原型级 InfoNCE 损失，增强当前域内类间分离：

$$\mathcal{L}_{\text{neg-intra}} = -\frac{1}{\mathbb{B}} \sum_{i=1}^{\mathbb{B}} \log \frac{\exp(\cos(\mathbf{f}_i, \mathbf{p}_{y_i}^{(t)}))}{\sum_{j=1}^{C_t} \exp(\cos(\mathbf{f}_i, \mathbf{p}_j^{(t)}))}$$

**跨域负样本抑制损失**。抑制新域特征与语义无关的历史原型的错误关联。定义 $g(\mathbf{f}, \mathbf{p}) = \exp(\cos(\mathbf{f}, \mathbf{p}))$，则：

$$\mathcal{L}_{\text{neg-cross}} = -\frac{1}{\mathbb{B}} \sum_{i=1}^{\mathbb{B}} \log \frac{g(\mathbf{f}_i, \mathbf{p}_{y_i}^{(t)})}{\sum_j g(\mathbf{f}_i, \mathbf{p}_j^{(t-1)}) \mathcal{K}[y_i \neq c_j^{(t-1)}]}$$

其中 $\mathcal{K}[\cdot]$ 为指示核函数，仅对语义不匹配的历史原型施加排斥力。

**类内紧凑性损失**。在同批次同类样本之间强化特征内聚性：

$$\mathcal{L}_{\text{intra}} = \frac{1}{|\mathcal{P}|} \sum_{(i,j) \in \mathcal{P}} [1 - \cos(\mathbf{f}_i, \mathbf{f}_j)]$$

其中 $\mathcal{P}$ 为批次内同类样本对的集合。

### 3.4 原型记忆与分类器

DK-DDIL 采用基于原型的增量分类器，支持动态标签扩展。对于类别 $c$，其原型为所有已见域中该类样本 L2 归一化特征的均值：

$$\mathbf{p}_c = \frac{1}{|\bigcup_{k=1}^{t} \mathcal{D}_k^c|} \sum_{(\mathbf{x}_i, y_i) \in \bigcup_{k=1}^{t} \mathcal{D}_k^c} \frac{f_\theta(\mathbf{x}_i)}{\|f_\theta(\mathbf{x}_i)\|_2}$$

推理时通过余弦相似度进行最近邻分类：

$$\hat{y} = \arg\max_{c \in \mathcal{V}_{1:t}} \cos(f_\theta(\mathbf{x}), \mathbf{p}_c)$$

该设计避免了传统线性分类器在标签空间动态扩展时的结构修改问题。

### 3.5 联合优化目标

DK-DDIL 的最终训练目标由交叉熵损失、秩正则化损失和 DCL 损失联合构成：

$$\mathcal{L} = \mathcal{L}_{\text{CE}} + \mathcal{L}_{\text{reg}} + \mathcal{L}_{\text{DCL}}$$

三者的协同作用体现在：$\mathcal{L}_{\text{CE}}$ 保证当前域的分类性能，$\mathcal{L}_{\text{reg}}$ 通过稀疏性约束实现自适应容量分配，$\mathcal{L}_{\text{DCL}}$ 则在特征空间巩固跨域知识、抑制灾难性遗忘。消融实验（Figure 3a）证实，移除 DAM 和 KIR 仅微调分类头（FT）会导致性能急剧下降，验证了自适应适配器与知识整合机制的不可或缺性。

## 实验与分析

### 主实验结果

DK-DDIL 在三个互补基准上均一致超越现有域增量学习方法，尤其在最终准确率 AT 上展现出显著的遗忘抑制能力。Table 1 汇总了核心定量结果。

![[assets/figures/papers/paper_list_l2119_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_DK_DDIL_Adaptive_Kn/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of state-of-the-art DIL methods on Skin Pathology Diagnosis, Cyst-X, and OfficeHome benchmarks. We report the average accuracy A and final accuracy AT , along with the proportion of trainable parameters (%) and statistical significance (p-value)*

**皮肤病理诊断 (Skin Pathology Diagnosis)。** 该基准包含七个时序域，标签空间动态演变且域间样本量高度不平衡（Figure 2）。DK-DDIL 取得 **A = 77.03% ± 0.52**，较最强基线 RanPAC (74.79% ± 0.10) 提升 +2.24 个百分点；**AT = 71.52% ± 1.04**，较 RanPAC (66.89% ± 0.09) 大幅提升 +4.63 个百分点。这一 AT 优势直接验证了 KIR 机制在无回放条件下有效缓解灾难性遗忘的核心能力。

**Cyst-X 3D MRI。** 在跨中心 MRI 囊肿分类任务上，DK-DDIL 取得 **A = 53.34%**、**AT = 51.08%**，分别领先 RanPAC +0.78 和 +2.88 个百分点。尽管该基准整体准确率偏低（反映 3D 医学影像域偏移的固有难度），DK-DDIL 在最终域上的遗忘程度显著低于所有对比方法，表明 DAM 的动态秩分配策略能适应不同成像协议下的特征漂移。

**OfficeHome。** 在自然图像域增量场景下，DK-DDIL 取得 **A = 84.35% ± 0.30**、**AT = 86.29% ± 0.19**，分别超出 RanPAC +2.13 和 +1.59 个百分点。值得注意的是，DK-DDIL 在该基准上 AT 高于 A，说明其知识整合策略不仅防止遗忘，还能通过跨域原型精炼提升最终域的分类性能。

**参数效率。** DK-DDIL 的可训练参数占比仅为 **0.26%**，略高于 L2P (0.15%) 但远低于 RanPAC (2.03%) 和其他适配器方法。在参数增量极小的约束下实现最优性能，验证了 DAM 仅激活必要秩成分的稀疏正则化策略的有效性。

**统计显著性。** 所有实验均进行 5 次重复，采用配对 t 检验（p < 0.05），DK-DDIL 在各基准上的优势具有统计显著性。

### 消融分析

Figure 3 系统剖析了各组件和关键超参数的贡献。

![[assets/figures/papers/paper_list_l2119_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_DK_DDIL_Adaptive_Kn/figures/004_Figure_3.jpg]]
*Figure 3: Ablation study of DK-DDIL. (a) Overall contribution on the key components*

**核心组件贡献 (Figure 3a)。** 移除 DAM 和 KIR、仅微调分类头（FT）导致性能急剧下降，A 和 AT 均大幅低于完整框架，说明自适应适配器与知识整合机制是 DK-DDIL 不可或缺的支柱。单独移除 DAM 或 KIR 均造成显著性能损失，但两者联合产生的增益超过各自贡献之和，表明动态秩调节与参数/原型级知识精炼之间存在正向协同效应。

**MKI 融合系数 α_init (Figure 3b)。** α_init = 0.3 时达到最佳稳定性-可塑性平衡。α_init 过小（<0.1）导致训练初期知识继承不足，新域学习缺乏历史约束；α_init 过大（>0.5）则过度偏向历史参数，限制模型对新域特征的适应能力。cosine 退火调度使融合强度随训练进程平滑衰减，避免了固定权重带来的刚性权衡。

**DAM 插入层位 (Figure 3c)。** 将 DAM 注入所有 ViT 层（All）带来最优整体性能，但仅注入奇数层（Odd）亦可接近最优，为资源受限场景提供了效率与效果的折中方案。注入前 6 层（0-5）优于后 6 层（6-11），表明浅层特征的自适应调节对跨域泛化更为关键。

**MKI 融合参数组 (Figure 3d)。** 在 MKI 中同时融合 A 与 B 矩阵未能进一步提升性能，仅融合 B 矩阵的简洁配置即可稳定集成历史知识。这与低秩适配理论一致——B 矩阵编码了任务特定的输出子空间，而 A 矩阵的输入投影对域变化更敏感，保留其独立性有利于维持当前域的可塑性。

**正则化权重 λ_reg (Figure 3e)。** 适中的 λ_reg 取得最佳性能：过低时稀疏性不足，过多秩成分被激活导致冗余；过高时过度抑制秩激活，限制模型灵活性。DAM 的稀疏正则化在容量分配与效率之间实现了精细调节。

**DAM 注入位置 (Figure 3f)。** 将 DAM 注入所有投影层（All Proj.）提供最一致的改进，优于仅注入 Query、Key 或 Value 投影。这表明对自注意力输出投影的秩调节比各注意力头的独立调节更具全局影响力。

**秩范围 (r_min, r_max) 敏感性 (Figure 3g)。** DK-DDIL 在较宽的 (r_min, r_max) 范围内保持稳定，较小的 r_min 配合理想的 r_max 能有效平衡灵活性与稳定性。过大的 r_min 导致基础秩冗余，过小的 r_max 则限制复杂域的适应能力。

### 失败模式与局限性

1. **模态局限性。** 当前方法针对图像模态（2D/3D 医学图像及自然图像）设计，未扩展到文本、时序或跨模态持续学习场景。在需要融合多模态信息的临床决策中，直接应用可能受限。

2. **预训练依赖。** DK-DDIL 深度依赖大规模预训练的 ViT-B/16 骨干。对于无高质量预训练模型的任务（如专用医学成像模态），从头训练可能导致 DAM 的秩调节机制失效或需要重新校准。

3. **超大规模域的可扩展性未验证。** 实验覆盖 4-7 个域，未在数十或数百个域的超大规模场景下验证 DAM 的动态秩分配策略是否会因历史 DAM 累积而导致存储和计算开销不可接受。

4. **阈值 τ 的敏感性。** 动态秩调整的离散化阈值 τ 和温度参数虽通过 STE 保持可微，但其初始化与域漂移的交互关系尚未充分探索，可能在极端域分布差异下需要手工调整。

5. **Cyst-X 基准的绝对性能偏低。** 尽管 DK-DDIL 相对基线有提升，但 3D MRI 跨中心场景下 AT 仅约 51%，表明域偏移极大时，仅靠低秩适配和原型对比仍不足以完全弥合分布鸿沟，可能需要更强的域对齐或数据增强策略。

### 补充图表

![[assets/figures/papers/paper_list_l2119_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_DK_DDIL_Adaptive_Kn/figures/002_Figure_2.jpg]]
*Figure 2: Sample distribution across seven sequential domains in the Skin Pathology Diagnosis setting. Each domain corresponds to a distinct clinical dataset or acquisition period, representing the temporal evolution of real-world dermatopathology practice. The y-axis is plotted on a logarithmic scale to emphasize cross-domain imbalance. Both the category composition and the sample size vary notably across domains—new lesion types (e.g., AK, SCC, MAL OTH) appear in later stages, whereas earlier domains contain fewer samples with a more limited set of lesion categories*

## 方法谱系与知识库定位

### 1. 与现有域增量学习方法的谱系关系

DK‑DDIL 处于**无排练、参数高效域增量学习（Domain‑Incremental Learning, DIL）** 的交叉点。与现有工作相比，其核心差异在于同时处理三个维度的动态性：**标签空间演化**、**域间高度异构**以及**模型容量的自适应分配**。

#### 1.1 与基于 Prompt 的方法对比

基于 Prompt 的 DIL 方法通过可学习的提示池来解耦域知识，典型代表包括 **L2P**（Wang et al., CVPR 2022）、**DualPrompt**（Wang et al., ECCV 2022）和 **CODA‑Prompt**（Smith et al., CVPR 2023）。这些方法在固定标签空间的设定下表现良好，但其提示选择机制通常依赖查询‑键匹配，难以应对标签空间动态扩张的场景。DK‑DDIL 摒弃了提示池，转而通过**动态秩适配器（DAM）** 在参数空间内直接分配域容量，从而天然支持增量标签扩展。

#### 1.2 与基于适配器的方法对比

基于适配器的 DIL 方法共享“冻结骨干 + 轻量残差”的设计哲学，但容量分配策略存在本质差异：

- **RanPAC**（McDonnell et al., NeurIPS 2023）和 **EASE**（Zhou et al., CVPR 2024）采用固定秩适配器或子空间集成，缺乏域感知的动态容量调节。
- **CL‑LoRA**（He et al., CVPR 2025）在持续学习中引入 LoRA，但使用固定的低秩配置，无法根据域复杂性灵活伸缩。
- **DUCT**（Zhou et al., CVPR 2025）通过双重巩固机制缓解遗忘，但其适配器融合为简单平均，缺乏 DK‑DDIL 中 MKI 的**余弦退火选择性融合**策略。

DK‑DDIL 的关键创新在于将 LoRA 的**秩选择从离散超参数转化为可学习的连续优化问题**：通过温度缩放 sigmoid 与直通估计器（STE）生成二元秩掩码，配合稀疏正则化，实现了每域细粒度的容量分配。这一设计使模型在简单域上自动压缩容量，在复杂域上灵活扩展，避免了手动调秩的低效。

#### 1.3 与基于剪枝和冻结的方法对比

**GC2**（Bayasi et al., TMI 2024）通过剪枝实现可泛化的持续分类，但其容量控制是二元的（保留/移除），缺乏 DAM 的连续秩缩放能力。**SimpleCIL**（Zhou et al., IJCV 2025）完全冻结骨干，仅增量训练分类头，虽然参数效率极高，但无法适应域分布偏移，在医学影像等高度异构场景下性能受限。DK‑DDIL 以仅 **0.26%** 的可训练参数（Table 1）实现了显著优于 SimpleCIL 的域适应能力，证明了**轻量动态适配**在效率与效果之间的更优平衡。

### 2. 知识库定位：核心机制与因果链路

DK‑DDIL 的知识贡献可凝练为一条**因果链路**：**域异质性 → 自适应容量分配 → 参数级融合 + 原型级精炼 → 稳定性‑可塑性平衡**。

#### 2.1 瓶颈识别

现有 DIL 方法在真实临床场景中面临双重瓶颈：
1. **固定容量假设**：假设所有域共享同一模型容量，无法应对域间数据规模、类别数和分布形态的巨大差异（Figure 2 展示了皮肤病理数据集中域间样本量的对数级差异）。
2. **缺乏跨域整合**：各域适配器独立训练或简单平均，导致特征漂移和灾难性遗忘。

#### 2.2 调节旋钮

DK‑DDIL 引入了三个相互协同的调节旋钮：

| 调节旋钮 | 机制 | 作用 |
|---------|------|------|
| **DAM 动态秩选择** | 可学习秩分数 + STE 二元掩码 + 稀疏正则化 | 根据域复杂性自动伸缩模型容量 |
| **MKI 选择性参数融合** | 余弦退火调度 + B 矩阵融合 | 在参数层面继承历史域知识，抑制干扰 |
| **DCL 原型级对比精炼** | 正对齐 + 域内/跨域负对比 + 类内紧凑 | 在特征空间巩固跨域判别性 |

这三个旋钮形成闭环：DAM 为每个域提供适当的容量基础，MKI 在参数空间平滑传递域不变知识，DCL 在特征空间精炼原型边界，三者共同抑制灾难性遗忘。

#### 2.3 决定性证据

- **DAM 的有效性**：消融实验（Figure 3a）显示，移除 DAM 和 KIR 仅微调分类头（FT）导致性能急剧下降，验证了自适应适配器与知识整合的不可或缺性。
- **MKI 与 DCL 的协同**：DK‑DDIL 在所有三个基准（Table 1）上的最终准确率 AT 均显著优于最强基线 RanPAC（皮肤病理 +4.63%，Cyst‑X +2.88%，OfficeHome +1.59%），直接证明了跨域特征漂移的有效缓解。
- **参数效率**：DK‑DDIL 仅使用 0.26% 的可训练参数，显著低于 RanPAC（2.03%），同时性能更优，验证了动态秩分配的高效性。

### 3. 适用边界与局限

#### 3.1 适用场景

DK‑DDIL 特别适用于以下条件同时满足的场景：
- **域序列高度异构**：域间数据规模、类别组成差异显著（如多中心医学影像）。
- **标签空间动态扩张**：新类别随时间涌现，旧类别持续存在。
- **无排练约束**：历史数据因隐私或存储限制不可复访。
- **预训练骨干可用**：依赖 ViT‑B/16 等大规模预训练模型提供强特征基座。

#### 3.2 已知局限

| 局限 | 详细说明 | 验证状态 |
|------|---------|---------|
| **模态单一** | 当前仅验证于 2D/3D 图像（皮肤病理、MRI、自然图像），未扩展到文本、语音等跨模态持续学习 | 需手动验证 |
| **预训练依赖** | 依赖 ViT‑B/16 预训练权重，对无预训练的任务可能不适用或需重新训练 | 论文明确提及 |
| **可扩展性未验证** | 未在极大规模数据集（如 >100 域）或超长域序列下测试 | 需手动验证 |
| **超参数敏感性** | 动态秩调整的阈值 τ 和稀疏正则化权重 λ_reg 仍可能引入额外的调参负担（Figure 3e,g 显示了性能对 λ_reg 和 (r_min, r_max) 的敏感性） | 论文通过消融提供了合理范围，但未给出自适应选择策略 |

### 4. 开放问题

1. **自适应阈值的收敛性**：DAM 中 STE 使用的固定阈值 τ 在训练过程中保持不变，其在不同域漂移程度下的鲁棒性如何？是否可设计可学习的阈值以进一步提升自动化程度？

2. **极端域差异下的稳定性**：当域间差异极大（如从皮肤病理切换到胸部 X 光）时，MKI 的参数融合策略是否仍能保持域不变子空间的有效传递？原型级对比在语义鸿沟过大时可能失效。

3. **融合策略的最优性**：MKI 当前仅融合 B 矩阵，理由是保留域不变子空间结构。但是否存在场景（如域间类别重叠度低）需要融合 A 矩阵或同时融合 AB？动态选择融合矩阵类型的机制值得探索。

4. **与视觉‑语言模型的结合**：DK‑DDIL 的原型分类器天然支持余弦相似度推理，与 CLIP 等视觉‑语言模型的嵌入空间高度兼容。如何将 DAM 的动态秩适配与语言引导的零样本域适应结合，是提升开放域泛化能力的潜在方向。

5. **计算开销的权衡**：DCL 需要维护和更新原型记忆库，其计算开销随类别数线性增长。在超大规模类别空间（如 >10K 类）下，原型存储和对比损失计算的效率需要进一步优化。

## 原文 PDF

![[paperPDFs/CVPR_2026/DK_DDIL_Adaptive_Knowledge_Retention_for_Dynamic_Domain_Incremental_Learning_in_Medical_Imaging.pdf]]
