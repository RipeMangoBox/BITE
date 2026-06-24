---
title: Dynamic Logits Adjustment and Exploration for Test-Time Adaptation in Vision Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dynamic_Logits_Adjustment_and_Exploration_for_Test_Time_Adaptation_in_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- DDLAE
- DLAETTAVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 动态逻辑值调整（DLA）基于在线预测统计估计目标分布，通过平衡函数重新校准类别logits，缓解类别不一致并暴露决策边界样本。
primary_logic: DLA在缓解类别偏差的同时，自然暴露对logit调整敏感的边界样本；配合语义与时间一致性引导的探索性缓存（CGEC），可以在不牺牲可靠性的前提下扩大测试分布覆盖，打破“高置信度→更偏向→更低探索”的自我强化循环。
claims:
- DPE在部分类别上准确率低于零样本CLIP，DLAE则显著减少类间方差（图1a）。
- DPE缓存中独特样本数很快饱和，DLAE则能持续引入更多样化样本（图1b）。
- DLA维护每类计数与置信度均值的运行估计，并使用平衡函数B(c)=exp(-α·p̂(c)·(1-d))调整logit。
- "CGEC主动纳入在DLA前后标签翻转的样本，并通过语义一致性（cos(t_ŷ_clip, t_ŷ_DLA)）和时间一致性（t⊤f_v > t⊤[now]f_v）过滤噪声。"
---

# Dynamic Logits Adjustment and Exploration for Test-Time Adaptation in Vision Language Models

> [!tip] 核心洞察
> DLA在缓解类别偏差的同时，自然暴露对logit调整敏感的边界样本；配合语义与时间一致性引导的探索性缓存（CGEC），可以在不牺牲可靠性的前提下扩大测试分布覆盖，打破“高置信度→更偏向→更低探索”的自我强化循环。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉语言模型测试时适应的动态逻辑值调整与探索 |
| 英文题名 | Dynamic Logits Adjustment and Exploration for Test-Time Adaptation in Vision Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_Dynamic_Logits_Adjustment_and_Exploration_for_Test-Time_Adaptation_in_Vision_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DLAE (Dynamic Logits Adjustment and Exploration) |
| Dataset | Cross-datasets generalization, Natural distribution shifts |

> [!tip] 效果简介
> - Cross-datasets generalization (Average over 10 datasets) 上，Top-1 Accuracy 64.81 (RN50) / 71.88 (ViT-B/16) vs Best competitor (see Table 1) (优于所有对比方法)。
> - Natural distribution shifts (OOD Average over 5 datasets) 上，Top-1 Accuracy 49.06 (RN50) / 65.76 (ViT-B/16) vs Best competitor (see Table 2) (优于所有对比方法)。

## 概述

**问题瓶颈**：现有视觉语言模型（VLM）的测试时适应（TTA）方法普遍依赖熵滤波筛选高置信度样本，导致类别预测偏差被持续放大，缓存覆盖不足，伪标签逐渐坍缩，难以探索低置信度区域。

**核心洞察**：通过在线的动态逻辑值调整（DLA）缓解类别偏差，同时自然暴露对logit调整敏感的决策边界样本；配合语义与时间一致性引导的探索性缓存（CGEC），在不牺牲可靠性的前提下扩大测试分布覆盖，打破“高置信度→更偏向→更低探索”的自我强化循环。

**方法定位**：DLAE（Dynamic Logits Adjustment and Exploration）属于基于缓存的VLM在线测试时适应范式，与**TPT**（Shu et al., NeurIPS 2022）的提示优化路线和**DPE**（Zhang et al., NeurIPS 2024）的缓存残差路线形成互补。其关键改进在于将“先筛选再学习”的被动缓存策略，转变为“先校准再探索”的主动边界挖掘机制。

**主要结果**：在跨数据集泛化（10个数据集平均）和自然分布偏移鲁棒性（5个OOD数据集平均）两项基准上，DLAE在ResNet-50和ViT-B/16两种CLIP骨干下均优于所有对比方法。消融实验表明，DLA和CGEC各自带来显著增益，二者联合使用效果最优。

## 背景与动机

视觉语言模型（VLM）的测试时适应（Test-Time Adaptation, TTA）旨在不依赖源域数据的前提下，使冻结的预训练模型在线适应目标域分布偏移。以CLIP为代表的VLM虽然展现了强大的零样本泛化能力，但在面对跨数据集偏移和自然分布变化时，其固定的文本原型难以捕捉目标域的类条件分布，导致性能显著下降。

### 现有方法的瓶颈

当前VLM测试时适应方法主要沿两条路径发展：基于提示微调的方法（如**CoOp** (Zhou et al., ICCV 2021)、**TPT** (Shu et al., NeurIPS 2022)）和基于缓存原型的方法（如**DPE** (Zhang et al., NeurIPS 2024)、**DualMem** (Zhang et al., CVPR 2024)）。其中，基于缓存的方法因其无需反向传播、计算高效而受到关注。然而，这些方法存在一个共同的结构性缺陷：**依赖熵滤波选择高置信度样本**。

这一策略在在线流式场景中引发了一个自我强化的恶性循环：
1. **类别预测偏差被放大**：模型倾向于对某些“易分类”类别反复给出高置信度预测，这些样本不断进入缓存并主导原型更新；
2. **缓存覆盖不足**：最小熵替换策略使缓存过早被低熵样本占据，难以接纳多样化的测试样本（见Figure 1b）；
3. **伪标签逐渐坍缩**：随着时间推移，模型对困难类别和决策边界附近样本的探索能力持续退化，部分类别的准确率甚至低于零样本CLIP基线（见Figure 1a黑框区域）。

简言之，**“高置信度→更偏向→更低探索”**的循环构成了现有缓存式TTA方法的核心瓶颈。

### 本文动机与核心洞察

本文的核心洞察在于：**缓解类别偏差与扩大测试分布覆盖并非两个独立目标，而是可以通过统一的logit空间校准机制协同实现**。

具体而言，当在logit空间施加类别特定的动态调整以缓解预测不一致时，那些对调整敏感的样本——即决策边界附近的低置信度样本——会被自然地“暴露”出来。这些边界样本恰好是缓存探索不足、模型最需要学习的区域。关键在于，如何在引入这些低置信度样本的同时，不牺牲伪标签的可靠性。

为此，本文提出**动态逻辑值调整与探索框架（DLAE）**，通过两个协同组件打破上述恶性循环：
- **动态逻辑值调整（DLA）**：基于在线预测统计实时估计目标域类别分布，通过平衡函数重新校准logits，缓解类别不一致并暴露边界样本；
- **一致性引导探索性缓存（CGEC）**：在保留高置信度样本的同时，主动纳入DLA前后标签翻转的边界样本，并通过语义一致性与时间一致性双重过滤机制控制噪声引入。

通过这种“调整暴露边界→一致性过滤探索→原型更新反哺校准”的协同设计，DLAE在不牺牲可靠性的前提下持续扩大测试分布覆盖，实现了对困难区域的稳定适应。

## 核心创新

### 问题诊断：置信度偏差与缓存坍缩的自我强化循环

现有基于缓存的VLM测试时适应方法（如 **DPE**，Zhang et al., NeurIPS 2024）普遍采用熵滤波策略——仅保留低熵（高置信度）样本进入缓存。这一机制在实践中引发两个相互耦合的退化现象：

1. **类别预测偏差被放大**：零样本CLIP本身存在显著的类间方差（见Figure 1a），熵滤波进一步筛选出模型已擅长的类别样本，导致缓存中类别分布严重失衡。在部分类别上，DPE的准确率甚至低于零样本CLIP基线（Figure 1a黑色虚线框区域），说明单纯依赖置信度筛选反而加剧了预测偏差。

2. **缓存覆盖快速饱和**：由于最小熵替换策略持续用“更简单”的样本替换缓存内容，缓存中独特样本数在测试流早期即趋于饱和（见Figure 1b），大量决策边界附近的困难样本被系统性排除，模型失去探索低置信度区域的能力。

这两个现象构成一个自我强化的恶性循环：高置信度筛选 → 缓存偏向简单类别 → 伪标签更偏向 → 低置信度区域被进一步忽视。

### 创新一：动态逻辑值调整（DLA）——在线去偏与边界暴露

DLA的核心思想是**在logit空间进行流式去偏，同时自然暴露决策边界样本**。其运作机制如下：

**在线目标分布估计**：DLA维护两组运行时统计量——每类的伪标签计数 $\mathbf{n}[c]$ 和置信度滑动均值 $\boldsymbol{\mu}[c]$。由此在线估计目标域的类别分布 $\hat{p}(c) = \mathbf{n}[c]/N$（Eq. 8）。

**平衡函数设计**：对于每个类别 $c$，DLA计算平衡因子：

$$B(c) = \exp(-\alpha \cdot \hat{p}(c) \cdot (1 - d)), \quad d = P_{clip}(\hat{y}_{clip}) - \boldsymbol{\mu}[\hat{y}_{clip}]$$

其中 $\hat{p}(c)$ 惩罚高频类别（缓解类别不平衡），$(1-d)$ 惩罚当前置信度高于历史均值的预测（缓解置信度偏差）。调整后的logit为 $s_{\mathrm{DLA}}^{c} = \mathbf{s}_{clip}^{c} \cdot B(c)$（Eq. 9-10）。

**关键洞察**：DLA的去偏操作在缓解类别偏差的同时，会**主动翻转部分样本的预测标签**。这些“翻转样本”恰好位于决策边界附近——它们对logit调整高度敏感，正是模型需要重点学习的困难样本。DLA因此扮演了“边界探测器”的角色，为后续的探索性缓存提供信号。

### 创新二：一致性引导探索缓存（CGEC）——安全地纳入边界样本

CGEC改变了传统缓存“仅保留高置信度样本”的策略，转而**在保留高置信度样本的同时，主动纳入DLA暴露的边界样本**，并通过双重一致性过滤器控制噪声风险。

**样本纳入策略**：CGEC同时接纳两类样本：
- 高置信度样本（传统策略）
- DLA前后标签翻转的样本（探索性策略）

**语义一致性过滤器（SCF）**：对翻转样本，用CLIP原始预测与DLA预测对应文本原型的余弦相似度调制其缓存熵值：

$$h \leftarrow h \cdot \exp(-\beta \cdot \cos(\mathbf{t}_{\hat{y}_{clip}}, \mathbf{t}_{\hat{y}_{DLA}}))$$

语义越一致（余弦相似度越高），熵值被压得越低，样本越容易被保留（Eq. 11）。这确保了纳入的翻转样本在语义上是合理的。

**时间一致性过滤器（TCF）**：对所有缓存样本，检测其特征与当前文本原型的对齐度是否随时间退化：

$$\mathbf{t}_{\hat{y}_{DLA}}^{\top}[0] \mathbf{f}_v > \mathbf{t}_{\hat{y}_{DLA}}^{\top}[\mathrm{now}] \mathbf{f}_v$$

若对齐度下降，则按驻留时长增加其熵值：$h \leftarrow h \cdot \exp(\eta (i_{\mathrm{now}} - i_{\mathrm{entry}}))$（Eq. 12-13），促使其被替换。这防止了因分布持续偏移而过时的样本长期占据缓存。

### 创新三：DLA与CGEC的协同机制

DLA和CGEC并非独立运作，而是形成闭环协同：

1. **DLA → CGEC**：DLA的去偏操作暴露边界样本（标签翻转），为CGEC提供探索信号；
2. **CGEC → DLA**：CGEC中积累的多样化样本通过原型残差学习（Eq. 2-3）更新视觉原型，使后续DLA的在线统计估计更加准确；
3. **双重一致性保障**：SCF确保纳入的边界样本语义合理，TCF确保缓存内容随分布演化而更新，避免噪声累积。

这种协同打破了“高置信度 → 更偏向 → 更低探索”的自我强化循环。消融实验证实：在DPEViT-B/16基线上单独添加DLA将准确率从69.40%提升至70.63%，进一步添加CGEC达到71.88%（Table 3a），验证了两个组件的互补性。

### 与现有方法的关键差异

| 设计维度 | 现有缓存方法（DPE/DualMem） | DLAE |
|---------|--------------------------|------|
| Logit校准 | 无，直接使用CLIP原始logit | 在线估计目标分布，动态调整logit |
| 缓存准入 | 仅低熵（高置信度）样本 | 高置信度 + DLA翻转的边界样本 |
| 缓存多样性 | 最小熵替换，快速饱和 | 探索性纳入 + 时间一致性淘汰 |
| 噪声控制 | 依赖置信度阈值 | 语义一致性 + 时间一致性双重过滤 |

值得注意的是，DLAE在**不增加缓存容量**的前提下实现了缓存多样性的显著提升（Figure 1b），这表明其改进源于样本选择策略的优化，而非简单的资源扩张。

## 整体框架

DLAE 面向 CLIP 视觉语言模型的在线测试时适应，采用全流式（streaming）处理范式：测试样本逐帧到达，模型仅基于当前样本和内部状态即时更新，不依赖离线批处理或未来数据。整体框架由冻结的 CLIP 编码器、动态逻辑值调整（DLA）、一致性引导探索缓存（CGEC）和原型残差学习四个核心模块级联构成，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2385_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Dynamic_Logits_Adju/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of the proposed DLAE framework. The framework consists of two main components: Dynamic Logits Adjustment (DLA) and a Consistency-Guided Exploratory Cache (CGEC). In the CLIP prediction stage, image and text encoders extract image features and textual prototypes initialized from hand-crafted prompts. DLA recalibrates logits using the estimated target prediction distribution to reduce prediction inconsistency and confidence bias. CGEC stores test samples while focusing more on those whose predicted labels change before and after DLA, encouraging exploration in low-confidence regions. Guided by semantic and temporal consistency, the cache updates image and textual prototypes th...*

**输入输出流**：对每个到达的测试图像，CLIP 图像编码器提取冻结的视觉特征 $\mathbf{f}_v$，文本编码器从手工提示中初始化各类文本原型 $\mathbf{t}_c$。零样本阶段，模型通过 $\mathbf{f}_v^{\top} \mathbf{t}_c$ 的点积计算原始 logit $\mathbf{s}_{clip}$。DLA 模块在线估计目标域类别分布，以平衡函数 $B(c)$ 重新校准 logit 得到 $\mathbf{s}_{DLA}$，缓解类别偏差并暴露决策边界附近的困难样本。CGEC 维护固定容量的按类缓存，不仅保留低熵高置信度样本，还主动纳入 DLA 前后标签翻转的边界样本，并通过语义一致性和时间一致性双过滤器控制缓存质量。缓存中的视觉特征经平均得到视觉原型 $\mathbf{v}_c$，与文本原型分别叠加可学习残差 $\Delta \mathbf{t}_c$、$\Delta \mathbf{v}_c$ 后 ℓ₂ 归一化。最终预测得分由 DLA 校准后的语义 logit 与亲和力调制的视觉原型相似度相加得到：$s_{DLAE}^{c} = s_{DLA}^{c} + \mathcal{A}(\mathbf{f}_v^{\top} \mathbf{v}_c)$。

**模块间因果联动**：DLA 的 logit 调整不仅提供去偏后的伪标签用于缓存准入判断，更是 CGEC 探索机制的触发信号——标签翻转样本正是 DLA 前后预测不一致的样本，这些样本通常位于类别决策边界，是传统熵滤波方法系统性忽略的低置信度区域。CGEC 通过语义一致性过滤器（SCF，以 $\cos(\mathbf{t}_{\hat{y}_{clip}}, \mathbf{t}_{\hat{y}_{DLA}})$ 衡量）和时间一致性过滤器（TCF，检测特征-原型对齐度是否随时间退化）对纳入的边界样本进行质量约束，避免噪声污染原型。原型残差学习则通过置信度感知校准损失 $\mathcal{L}_{conf}$ 和对称跨模态对齐损失 $\mathcal{L}_{align}$ 驱动在线适应，形成“去偏→探索→学习→更准的去偏”的正反馈循环。Figure 1 的动机实验表明，这一设计有效打破了现有方法（如 DPE）中“高置信度筛选→类别偏差放大→缓存过早饱和→探索停滞”的自我强化困境。

## 核心模块与公式推导

DLAE 框架由两个关键模块构成：**动态逻辑值调整（DLA）** 与 **一致性引导的探索性缓存（CGEC）**。DLA 负责在线重新校准类别 logits，缓解预测偏差并暴露决策边界附近的困难样本；CGEC 则在保留高置信度样本的基础上，主动纳入 DLA 前后标签翻转的边界样本，通过语义与时间一致性约束控制缓存质量，从而扩大测试分布覆盖。

### 3.1 动态逻辑值调整（DLA）

现有基于缓存的测试时适应方法（如 **DPE**，Zhang et al., NeurIPS 2024）依赖最小熵替换策略，仅保留高置信度样本，导致缓存过早被简单样本占据，类别预测偏差被持续放大。DLA 的核心思路是：利用在线预测统计实时估计目标域类别分布，并对 CLIP 原始 logits 施加类别特定的缩放，从而抑制高频类别的过度自信，同时提升低频类别的响应。

DLA 为每个类别 $c$ 维护两个运行时估计量：伪标签计数 $\mathbf{n}[c]$ 和运行平均置信度 $\boldsymbol{\mu}[c]$。由计数可得目标域经验类别分布：

$$\hat{p}(c) = \frac{\mathbf{n}[c]}{N}, \quad N = \sum_{c'=1}^{C} \mathbf{n}[c'] \tag{8}$$

平衡函数 $B(c)$ 综合了类别频率和当前预测置信度与历史均值的偏差：

$$B(c) = \exp(-\alpha \cdot \hat{p}(c) \cdot (1 - d)), \quad d = P_{clip}(\hat{y}_{clip}) - \boldsymbol{\mu}[\hat{y}_{clip}] \tag{9}$$

其中 $\alpha$ 为调整强度，$d$ 衡量当前预测置信度偏离历史均值的程度。当某类别被频繁预测（$\hat{p}(c)$ 高）且当前置信度高于历史均值（$d>0$）时，$B(c)$ 变小，抑制该类别 logit；反之则放大。最终 DLA 调整后的 logit 为：

$$s_{\mathrm{DLA}}^{c} = \mathbf{s}_{clip}^{c} \cdot B(c) \tag{10}$$

这一校准操作在缓解类别偏差的同时，自然暴露了对 logit 调整敏感的边界样本——这些样本在 DLA 前后的预测标签往往发生翻转，成为 CGEC 的重点探索对象。

### 3.2 一致性引导的探索性缓存（CGEC）

CGEC 在传统高置信度缓存的基础上，额外纳入 DLA 前后标签翻转的样本（即 $\hat{y}_{clip} \neq \hat{y}_{DLA}$），并通过双重一致性过滤器控制噪声引入。

**语义一致性过滤器（SCF）** 对翻转样本施加语义约束：若 CLIP 预测标签的文本原型与 DLA 预测标签的文本原型在语义空间中高度相似，则翻转可能源于决策边界附近的合理波动而非随机噪声。SCF 通过降低此类样本的缓存熵值，使其更可能被保留：

$$h \leftarrow h \cdot \exp(-\beta \cdot \cos(\mathbf{t}_{\hat{y}_{clip}}, \mathbf{t}_{\hat{y}_{DLA}})) \tag{11}$$

其中 $\beta$ 控制语义一致性权重，余弦相似度越高，熵值衰减越大。

**时间一致性过滤器（TCF）** 对缓存中所有样本进行时序监控：检测样本特征对当前文本原型的对齐度是否较初始时刻下降。若下降，说明该样本与当前模型状态不再一致，应被淘汰：

$$\mathbf{t}_{\hat{y}_{DLA}}^{\top}[0] \mathbf{f}_v > \mathbf{t}_{\hat{y}_{DLA}}^{\top}[\mathrm{now}] \mathbf{f}_v \tag{12}$$

触发时间不一致惩罚时，按样本驻留时步增加其熵值：

$$h \leftarrow h \cdot \exp(\eta (i_{\mathrm{now}} - i_{\mathrm{entry}})) \tag{13}$$

其中 $\eta$ 为时间衰减系数，$i_{\mathrm{now}}$ 和 $i_{\mathrm{entry}}$ 分别为当前时步和样本入缓存时步。

### 3.3 最终预测得分

DLAE 的最终预测将 DLA 校准后的语义 logit 与 CGEC 维护的视觉原型相似度相结合。视觉原型 $\mathbf{v}_c$ 由缓存中各类图像特征的均值构成，并通过可学习残差 $\Delta \mathbf{v}_c$ 进行自适应调整。最终得分为：

$$s_{\mathrm{DLAE}}^{c} = s_{\mathrm{DLA}}^{c} + \mathcal{A}(\mathbf{f}_{v}^{\top} \mathbf{v}_{c})$$

其中 $\mathcal{A}(\cdot)$ 为亲和力调制函数，预测标签取最大得分类别：$\hat{y}_{\mathrm{DLAE}} = \arg\max_{c} s_{\mathrm{DLAE}}^{c}$。

**消融实验**（Table 3）验证了各模块的独立贡献：在 ViT-B/16 骨干上，仅将 DLA 添加至 DPE 基线即可将平均准确率从 69.40% 提升至 70.63%；进一步引入 CGEC 后达到 71.88%。**超参数分析**（Table 4, Figure 3）表明，DLA 调整强度 $\alpha$ 在约 2.0 时最优，时间衰减系数 $\eta$ 在 0.01 附近时多数数据集表现最佳。

### 补充图表

![[assets/figures/papers/paper_list_l2385_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Dynamic_Logits_Adju/figures/001_Figure_1.jpg]]
*Figure 1: (a) Per-class accuracy (top-1) on the target stream for CLIP in zero-shot mode, DPE as a cache-based TTA method, and our DLAE. CLIP exhibits large per-class variance. The black dashed box highlights classes where DPE underperforms and even falls below the zero-shot baseline, while our method achieves more consistent accuracy across classes. (b) Number of distinct target samples entering the cache over the test stream as the time step increases. Both DPE and DLAE use caches with the same fixed capacity and update them throughout the stream. However, the minimum-entropy replacement policy of DPE causes the cache to be dominated by low-entropy samples, preventing many diverse samples from ente...*

## 实验与分析

### 跨数据集泛化与分布偏移鲁棒性

DLAE在跨数据集泛化与自然分布偏移两个维度上均取得了最优性能。Table 1报告了10个跨数据集泛化基准上的平均Top-1准确率：使用ResNet-50骨干时达到**64.81%**，使用ViT-B/16骨干时达到**71.88%**，全面超越CoOp（Zhou et al., ICCV 2021）、TPT（Shu et al., NeurIPS 2022）、DPE（Zhang et al., NeurIPS 2024）、DualMem（Zhang et al., CVPR 2024）和BayesianTTA（Zhou et al., CVPR 2025）等对比方法。Table 2展示了在5个自然分布偏移数据集（包含图像损坏与对抗样本）上的平均鲁棒性：ResNet-50下为**49.06%**，ViT-B/16下为**65.76%**，同样优于所有对比方法。这表明DLAE在域内微调不可行的开放场景中，能够稳定地提升VLM的泛化与鲁棒性。

### 消融研究：DLA与CGEC的独立贡献

Table 3的消融实验逐步验证了各组件的有效性。以DPEViT-B/16基线（69.40%）为起点：

- **仅添加DLA**：准确率提升至**70.63%**（+1.23%），证明在线逻辑值校准本身即可缓解类别偏差带来的性能退化。
- **进一步添加CGEC**：准确率达到**71.88%**（+1.25%），表明探索性缓存在DLA暴露的决策边界样本上获得了额外增益。

这一递增趋势与Figure 1的动机分析一致：DLA缩小了类别间准确率方差（Figure 1a），而CGEC使缓存中独特样本数持续增长而非过早饱和（Figure 1b），两者协同打破了“高置信度→更偏向→更低探索”的自我强化循环。

### 超参数敏感性

DLAE的核心超参数在不同取值下表现稳健。Table 4在DTD数据集上的分析显示，DLA调整强度α在**2.0**附近达到最优（58.86%），过大的α会过度抑制高频类而引入新的偏差，过小的α则校准不足。语义一致性权重β同样存在合理区间，过低时噪声样本混入缓存，过高时边界样本被过度过滤，均会削弱探索性缓存的收益。

Figure 3展示了时间衰减系数η的敏感性。η控制缓存中时间不一致样本的熵值衰减速度（见Eq. 13）。当η≈**0.01**时，模型在多数数据集上表现最佳；η过小导致过时样本滞留，η过大则可能过早驱逐仍有价值的样本。该参数在不同数据集上的最优值高度一致，表明时间一致性过滤机制具有良好的跨域稳定性。

### 关键洞察与失败模式

DLAE的核心优势源于两个因果机制的耦合：

1. **DLA的校准-暴露双重效应**：平衡函数$B(c) = \exp(-\alpha \cdot \hat{p}(c) \cdot (1 - d))$不仅根据在线估计的类别分布$\hat{p}(c)$抑制高频类的logit，还通过置信度偏差项$(1 - d)$（当前置信度与历史均值的偏差）自适应调节强度。这使得被CLIP高置信度误分类的样本在DLA后标签翻转，自然暴露为边界样本。

2. **CGEC的双重一致性过滤**：语义一致性过滤器（SCF）通过$\cos(\mathbf{t}_{\hat{y}_{clip}}, \mathbf{t}_{\hat{y}_{DLA}})$衡量翻转前后文本原型的语义接近程度，仅保留语义连贯的翻转样本；时间一致性过滤器（TCF）检测$\mathbf{t}_{\hat{y}_{DLA}}^{\top}[0] \mathbf{f}_v > \mathbf{t}_{\hat{y}_{DLA}}^{\top}[\mathrm{now}] \mathbf{f}_v$，当缓存样本对当前原型的对齐度下降时施加时间惩罚。两者共同确保探索不会引入噪声。

需要手动验证的潜在失败模式：当目标域类别分布与源域严重偏离且DLA的在线估计收敛缓慢时，初始阶段的校准可能不准确，导致CGEC在早期纳入错误翻转样本。论文未报告流式适应初期的逐步性能曲线，该场景下的鲁棒性需要进一步确认。

### 补充图表

![[assets/figures/papers/paper_list_l2385_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Dynamic_Logits_Adju/figures/003_Table_1.jpg]]
*Table 1: Top-1 accuracy (in %) on cross-datasets generalization. For all evaluated methods, we report the results on both ResNet-50 and ViT-B/16 visual backbones of CLIP*

![[assets/figures/papers/paper_list_l2385_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Dynamic_Logits_Adju/figures/004_Table_2.jpg]]
*Table 2: Top-1 accuracy (in %) on robustness to natural distribution shifts. For all evaluated methods, we report the results on both ResNet-50 and ViT-B/16 visual backbones of CLIP*

![[assets/figures/papers/paper_list_l2385_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Dynamic_Logits_Adju/figures/006_Table_3.jpg]]
*Table 3: Ablation study on components of (a) Dynamic Logits Adjustment and Exploration, (b) Dynamic Logits Adjustment, and (c) Consistency-Guided Exploratory Cache*

![[assets/figures/papers/paper_list_l2385_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Dynamic_Logits_Adju/figures/005_Figure_3.jpg]]
*Figure 3: Sensitivity analysis of the parameter η, which is defined in Eq. 13. The figure shows how different values of η affect model performance across various datasets*

![[assets/figures/papers/paper_list_l2385_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Dynamic_Logits_Adju/figures/007_Table_4.jpg]]
*Table 4: Sensitivity analysis of α in Eq. 9 and β in Eq. 11 on the DTD dataset*

## 方法谱系与知识库定位

### 技术谱系：从提示适应到缓存探索的演进

DLAE 的工作建立在视觉语言模型测试时适应（TTA）的三条技术路线上，并针对其各自的瓶颈进行了系统性改进。

**提示学习路线** 的代表工作包括 **CoOp**（Zhou et al., ICCV 2021）和 **TPT**（Shu et al., NeurIPS 2022）。CoOp 通过线下可学习的软提示替换手工模板，但需要标注数据且无法适应未见分布。TPT 将提示优化引入测试时，通过对增广视图的熵最小化在线更新提示，但其优化目标仅依赖置信度，容易在类别不均衡的目标域上放大预测偏差。

**缓存与原型路线** 以 **DPE**（Zhang et al., NeurIPS 2024）和 **DualMem**（Zhang et al., CVPR 2024）为代表。这类方法在测试流上维护一个固定容量的记忆缓存，按最小熵策略保留样本并学习残差原型。DLAE 的分析表明，这一策略存在一个自我强化的负面循环：低熵样本被优先保留 → 缓存被简单样本占据 → 模型在简单类别上过拟合 → 困难样本的熵值持续偏高 → 更难进入缓存。Figure 1(b) 直接展示了这一现象——DPE 缓存中独特样本数很快饱和，而 DLAE 在同一固定容量下能持续纳入更多样化的样本。

**贝叶斯适应路线** 以 **BayesianTTA**（Zhou et al., CVPR 2025）为代表，通过贝叶斯推断对预测不确定性进行建模。这类方法在理论上更完备，但计算开销较大，且未直接解决缓存覆盖不足的问题。

DLAE 的关键突破在于打破了上述负面循环。其核心洞察是：**类别偏差的缓解与探索性缓存的构建可以互为因果**——动态逻辑值调整（DLA）在缓解类别偏差的同时，自然暴露对 logit 调整敏感的决策边界样本；这些翻转样本正是探索性缓存（CGEC）的目标猎物，而更丰富的缓存又为 DLA 提供了更准确的在线统计量。这一双向增益机制是 DLAE 区别于所有前述方法的本质特征。

### 核心机制定位：DLA 与 CGEC 的协同逻辑

DLAE 的贡献需要从两个组件的协同关系来理解，而非孤立地看待每个模块。

**DLA 的角色超越“去偏”**。传统的 logit 校准方法（如类频率加权或后处理重缩放）仅试图修正类别先验偏差。DLA 的设计更深一层：其平衡函数 $B(c) = \exp(-\alpha \cdot \hat{p}(c) \cdot (1 - d))$ 不仅考虑类别频率 $\hat{p}(c)$，还引入预测可靠性偏差 $d = P_{clip}(\hat{y}_{clip}) - \boldsymbol{\mu}[\hat{y}_{clip}]$。这意味着 DLA 对“当前预测置信度显著偏离历史均值”的样本施加更强的调整，从而系统性暴露模型不确定的边界样本。这些样本的标签在 DLA 前后发生翻转，成为 CGEC 探索的明确信号。

**CGEC 的探索是有约束的**。与简单的“纳入低置信度样本”策略不同，CGEC 通过两道过滤器控制探索的质量边界：（1）语义一致性过滤器（SCF）要求翻转样本的 CLIP 预测文本原型与 DLA 预测文本原型具有足够高的余弦相似度，过滤掉语义上不合理的翻转；（2）时间一致性过滤器（TCF）检测缓存样本对当前文本原型的对齐度是否随时间退化，若退化则通过 $h \leftarrow h \cdot \exp(\eta (i_{\mathrm{now}} - i_{\mathrm{entry}}))$ 加速淘汰。这两道过滤器使得探索不会退化为噪声注入。

**与自训练范式的区别**。DLAE 不属于传统的伪标签自训练框架。它不维护指数移动平均的教师模型，也不依赖多次前向传播的一致性投票。其适应信号来自两个源头：DLA 在线统计量驱动的 logit 空间校准，以及 CGEC 中残差原型的跨模态对齐损失 $\mathcal{L}_{align}$ 和置信度校准损失 $\mathcal{L}_{conf}$。这种设计的优势在于计算开销低，适合流式测试场景。

### 适用边界与局限

**适用场景**。DLAE 的设计假设测试流中存在类别分布不均和样本难度差异，且这些偏差可通过在线统计量被逐步估计。在跨数据集泛化（Table 1，10 个数据集的平均）和自然分布偏移（Table 2，5 个 OOD 数据集的平均）两类场景下，DLAE 在两个骨干网络（ResNet-50 和 ViT-B/16）上均优于所有对比方法，表明这一假设在常见迁移场景中成立。

**关键超参数敏感度**。DLA 的调整强度 α 在 DTD 数据集上的最优值约为 2.0（Table 4），过大的 α 会导致过度压制高频类别，过小则去偏效果不足。时间衰减系数 η 的最优值在 0.01 附近（Figure 3），但其敏感度在不同数据集上存在差异，需要手动验证的部分是：论文未提供跨数据集的 η 调参指南，实际部署时可能需要根据测试流的长度和分布漂移速度进行网格搜索。

**未充分验证的边界**。以下方面在论文中缺乏直接实验证据：
- **极端类别不均衡**（如长尾分布中尾类占比低于 1%）：DLA 的在线估计可能因样本量过小而高度噪声，平衡函数的可靠性下降。
- **开放集测试流**（包含训练时未见类别）：DLA 和 CGEC 均依赖封闭类别的 logit 空间，未见类别的处理策略未定义。
- **持续概念漂移**（测试分布随时间缓慢变化）：TCF 的时间衰减机制假设初始原型是可靠的参照点，但在持续漂移下这一参照可能逐渐失效。
- **计算开销的精确测量**：论文声称 DLAE 适用于流式场景，但未报告与 DPE、TPT 等方法的推理延迟或内存占用的定量对比。

### 开放问题

1. **DLA 的估计稳定性**：当测试流的前期样本恰好集中在少数类别时，DLA 的在线计数 n 和置信度均值 μ 可能被错误初始化，导致早期阶段的 logit 调整方向错误。这种“冷启动”偏差是否会随时间自纠正，以及需要多少样本才能收敛，论文未给出分析。

2. **CGEC 的容量敏感性**：CGEC 的探索效果依赖于缓存容量是否足以容纳足够的翻转样本。在类别数 C 很大的场景下，固定缓存可能再次面临覆盖不足的问题。是否存在容量与类别数的理论关系，是一个开放问题。

3. **与提示优化的可组合性**：DLAE 在冻结的 CLIP 编码器上操作，仅学习残差原型。如果结合 TPT 的提示优化（同时更新文本编码器），DLA 的在线统计量是否会因文本空间的漂移而失效？两者的联合训练可能带来进一步的增益，但也可能引入新的不稳定因素。

4. **翻转信号的可靠性**：CGEC 的核心假设是“DLA 前后标签翻转的样本是值得探索的边界样本”。但在 DLA 本身尚未收敛的早期阶段，翻转可能由噪声而非真实的决策边界不确定性引起。论文未分析翻转样本的伪标签准确率随时间的演化。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dynamic_Logits_Adjustment_and_Exploration_for_Test_Time_Adaptation_in_Vision_Language_Models.pdf]]
