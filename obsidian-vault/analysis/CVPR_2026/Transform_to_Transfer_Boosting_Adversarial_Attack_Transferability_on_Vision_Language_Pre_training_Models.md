---
title: "Transform to Transfer: Boosting Adversarial Attack Transferability on Vision-Language Pre-training Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Transform_to_Transfer_Boosting_Adversarial_Attack_Transferability_on_Vision_Language_Pre_training_Models.pdf
project_link: null
code_link: null
aliases:
- TTAT
- TTBAATVLPTM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 可学习的块级变换组合策略（自适应选择最优变换）与增强的集成梯度（利用实现不变性减少源模型过拟合）共同大幅提升迁移性。
primary_logic: 不同图像对变换操作具有不同敏感性，采用可学习的逐块变换能最大化输入多样性；而集成梯度通过沿多条变换路径采样，可降低梯度相似性，有效缓解对源模型的过拟合。
claims:
- 在Flickr30K图像-文本检索任务上，TTA跨模型迁移的成功率显著高于SGA、LSSA、DRA等现有方法。
- 在从CLIP_CNN到ALBEF的刁难迁移场景中，TTA的TRR@1达到55.16%，比LSSA提升23.77个百分点。
- 消融实验表明，可学习变换与增强集成梯度两个组件协同作用，组合使用达到最佳攻击效果。
- Flickr30K Image-Text Retrieval (ALBEF→CLIP_CNN) 上 TRR@1 = 55.16
---

# Transform to Transfer: Boosting Adversarial Attack Transferability on Vision-Language Pre-training Models

> [!tip] 核心洞察
> 不同图像对变换操作具有不同敏感性，采用可学习的逐块变换能最大化输入多样性；而集成梯度通过沿多条变换路径采样，可降低梯度相似性，有效缓解对源模型的过拟合。

| 字段 | 内容 |
|------|------|
| 中文题名 | 变换以迁移：增强视觉-语言预训练模型对抗攻击的迁移性 |
| 英文题名 | Transform to Transfer: Boosting Adversarial Attack Transferability on Vision-Language Pre-training Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Transform_to_Transfer_Boosting_Adversarial_Attack_Transferability_on_Vision-Language_Pre-training_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Transform to Transfer Attack (TTA) |
| Dataset | Flickr30K Image-Text Retrieval, MSCOCO Image Captioning |

> [!tip] 效果简介
> - Flickr30K Image-Text Retrieval (ALBEF→CLIP_CNN) 上，TRR@1 55.16 vs LSSA (+23.77)；IRR@1 66.42 vs LSSA (+22.36)。
> - Flickr30K Image-Text Retrieval (ALBEF→CLIP_ViT) 上，TRR@1 92.27 vs LSSA (显著低于此值) (显著优于所有对比方法)。
> - MSCOCO Image Captioning (跨任务迁移) 上，BLEU-4 12.1 vs Original Baseline (大幅降低（越低攻击效果越好）)。

## 概述

视觉-语言预训练（VLP）模型在下游任务中展现出强大能力，但其对抗鲁棒性不足的问题日益凸显。当前针对VLP模型的对抗攻击方法在提升跨模型迁移性时面临一个核心瓶颈：**过度依赖源模型的特定梯度，且采用的输入变换策略固定、有限，导致对源模型过拟合，难以泛化至不同架构的目标模型**。

针对上述问题，本文提出 **Transform to Transfer Attack (TTA)** 方法。其核心洞察在于两点：第一，不同图像对变换操作的敏感性存在差异，采用可学习的块级变换组合能够自适应地最大化输入多样性；第二，沿多条变换路径采样的增强集成梯度（Boosted IG）可有效降低梯度相似性，缓解对源模型的过拟合。通过将可学习变换与增强集成梯度协同使用，TTA 显著提升了对抗样本的跨模型迁移能力。

实验结果表明，TTA 在图像-文本检索任务上大幅超越现有方法。在从 ALBEF 到 CLIP_CNN 的刁难迁移场景中，TTA 的 TRR@1 达到 **55.16%**，相较 LSSA 提升 **23.77 个百分点**；IRR@1 达到 **66.42%**，提升 **22.36 个百分点**。在 MSCOCO 图像描述任务上的跨任务迁移实验中，TTA 同样展现出优异的攻击效果。消融实验进一步验证了可学习变换与增强集成梯度两个组件的协同作用。

## 背景与动机

视觉-语言预训练（VLP）模型在图像-文本检索、视觉定位、图像描述等下游任务中取得了显著成功。然而，这些模型对对抗样本的脆弱性已成为其安全部署的关键隐患。对抗攻击通过在输入上施加人眼不可察觉的扰动，使模型产生错误输出。在VLP的多模态场景中，攻击者可以同时扰动图像和文本模态，造成跨模态的连锁失效，这对实际应用构成了更严峻的威胁。

**核心瓶颈：现有攻击方法的迁移性受限。** 对抗攻击的迁移性——即针对源模型生成的对抗样本能够同样欺骗其他目标模型的能力——是评估攻击实用性的关键指标。当前针对VLP的先进攻击方法，如**SGA**（Lu et al., ICCV 2023）、**LSSA**（Liu et al., NAACL 2025）和**DRA**（Gao et al., ECCV 2024），虽然在白盒攻击场景下表现优异，但在跨模型迁移性上仍存在两个根本性缺陷：

1. **固定且有限的输入变换策略**：现有方法依赖预定义的变换操作（如SGA的缩放变换、LSSA的局部洗牌），这些操作对所有图像一视同仁，忽略了不同图像对变换操作的敏感性差异。实际上，不存在一种对所有图像都最优的单一变换组合，而最有效的变换策略本质上涉及块级操作。

2. **对源模型梯度的过度依赖**：现有方法的优化过程强依赖于源模型特定的梯度信息，导致生成的对抗扰动过拟合于源模型的决策边界。当迁移到架构不同的目标模型时，攻击效果急剧下降。如Figure 2所示，即使将集成梯度（Integrated Gradients）与SGA结合，沿积分路径的采样点梯度相似性仍然过高，表明源模型过拟合问题未得到有效缓解。

**本文动机：通过可学习变换与增强集成梯度实现迁移性突破。** 针对上述瓶颈，本文提出**Transform to Transfer Attack (TTA)**，核心动机在于两个维度的创新：

- **自适应输入多样性**：引入可学习的块级变换机制，使模型能够针对每张图像自适应选择最优的变换组合，最大化输入多样性，从而生成更具泛化性的对抗样本。
- **缓解源模型过拟合**：采用增强集成梯度（Boosted Integrated Gradients, BIG），利用集成梯度的实现不变性（implementation invariance），通过沿多条变换路径采样来降低梯度相似性，减少对抗扰动对源模型特定特征的依赖。

这两种机制的协同作用使得TTA能够在保持白盒攻击强度的同时，显著提升跨模型、跨任务的迁移能力，为VLP模型的鲁棒性评估提供了更强的攻击基准。

## 核心创新

TTA 的核心创新在于从两个维度打破了现有攻击对源模型的过度依赖：**可学习的块级变换策略**与**增强集成梯度（Boosted Integrated Gradient, BIG）**。二者协同作用，使对抗样本的迁移性得到显著提升。

### 1. 从固定变换到可学习块级变换

现有方法（如 **SGA** (Lu et al., ICCV 2023) 的缩放变换、**LSSA** (Liu et al., NAACL 2025) 的局部洗牌）采用固定、有限的输入变换策略来增强样本多样性。然而，不同图像对变换操作的敏感性存在差异，不存在对所有图像都最优的单一变换组合（Section 3.1）。TTA 将变换策略从“固定选择”变为“自适应学习”，其关键设计如下：

- **块级操作空间**：维护 $M$ 种分块策略 $\{b_1, b_2, ..., b_m\}$ 和 $N$ 种变换操作 $\{t_1, t_2, ..., t_n\}$，并赋予可学习的概率分布 $P_b$ 和 $P_t$。图像 $x$ 经分块策略 $b_i$ 被划分为 $K$ 个图像块 $x^1 \oplus x^2 \oplus \cdots \oplus x^k$，每个块再依次应用 $L$ 个变换操作 $t_L^k(x^k) = t_1^k \otimes t_2^k \otimes \cdots \otimes t_l^k$，最终得到整体变换 $o(x) = t_L^K(b_i(x))$（Equation 1–3）。
- **自适应选择**：通过可学习参数，模型在攻击过程中自动选择对当前图像最有效的分块方式与变换组合，最大化输入多样性，从而突破固定变换策略的局限性。

### 2. 从标准梯度到增强集成梯度

**DRA** (Gao et al., ECCV 2024) 通过对抗轨迹插值缓解过拟合，但其梯度计算仍高度依赖源模型。TTA 引入增强集成梯度 BIG，利用集成梯度的实现不变性来降低梯度相似性，减少对源模型的过拟合：

$$BIG_i(f_I, f_T, x, B, c) = (x_i - B_i) \times \sum_{w=1}^{Q_O} \frac{\partial \mathcal{L}(f_I, f_T, o_w(x), B, c)}{\partial x_i} \times \frac{1}{Q_O}$$

其中 $B$ 为边界图像，$Q_O$ 为变换路径数量。BIG 沿多条由可学习变换生成的路径采样并聚合梯度，而非仅依赖当前图像的单一路径。Figure 2 的证据表明，SGA 结合标准集成梯度时，沿积分路径的采样点梯度相似性过高，仍会导致源模型过拟合；BIG 通过可学习变换打破这种相似性，使梯度方向更具泛化性。

### 3. 协同效应

消融实验（Figure 4）证实，可学习变换（LT）与增强集成梯度（BIG）单独使用均可提高迁移性，但二者组合时才达到最优攻击效果。这一协同作用在刁难迁移场景中尤为突出：从 ALBEF 到 CLIP_CNN 的跨架构攻击中，TTA 的 TRR@1 达到 55.16%，比 LSSA 提升 23.77 个百分点（Table 1）。

## 整体框架

TTA（Transform to Transfer Attack）是一个面向视觉-语言预训练（VLP）模型的多模态对抗攻击框架，其整体pipeline如Figure 3所示。框架的核心设计思想是：**通过可学习的图像变换增强输入多样性，同时利用增强集成梯度缓解对源模型的过拟合**，从而大幅提升对抗样本的跨模型迁移能力。

### 输入与输出流

框架的输入包含三个要素：**原始图像**、**原始文本描述**以及一个**基线图像**（baseline image，通常为纯黑或纯白图像）。输出为同时包含图像扰动和文本扰动的多模态对抗样本。整个攻击过程以白盒方式在源模型上生成对抗样本，随后将其迁移至黑盒目标模型进行攻击评估。

### 图像模态攻击管线

图像模态的攻击管线由两个核心模块串联构成：

1. **可学习图像变换模块**：对输入图像执行缩放操作后，应用可学习的块级变换策略。具体而言，框架维护两个候选列表——$M$种分块策略$\{b_1, b_2, ..., b_M\}$和$N$种变换操作$\{t_1, t_2, ..., t_N\}$，以及对应的概率分布$P_b$和$P_t$。对于每张图像，系统从$P_b$中采样一种分块策略$b_i$将图像划分为$K$个图像块，再对每个图像块从$P_t$中采样$L$个变换操作依次应用。整体变换过程可表示为：
   $$o(x) = t_L^K(b_i(x)) = t_L^1(x^1) \oplus t_L^2(x^2) \oplus \cdots \oplus t_L^K(x^K)$$
   其中$b_i(x) = x^1 \oplus x^2 \oplus \cdots \oplus x^K$表示分块，$t_L^k(x^k) = t_1^k \otimes t_2^k \otimes \cdots \otimes t_L^k$表示对第$k$个图像块依次应用$L$个变换。概率分布$P_b$和$P_t$在攻击过程中通过梯度反向传播进行学习，使得框架能够自适应地为每张图像选择最优的变换组合。

2. **增强集成梯度（BIG）生成模块**：基于变换模块生成的多样化变体，计算增强集成梯度以生成图像对抗扰动。BIG的核心公式为：
   $$BIG_i(f_I, f_T, x, B, c) = (x_i - B_i) \times \sum_{w=1}^{Q_O} \frac{\partial \mathcal{L}(f_I, f_T, o_w(x), B, c)}{\partial x_i} \times \frac{1}{Q_O}$$
   其中$B$为基线图像，$o_w(x)$为第$w$条变换路径下的图像变体，$Q_O$为变换路径总数。损失函数$\mathcal{L}$计算变换后图像嵌入与文本嵌入的余弦相似度：
   $$\mathcal{L}(f_I, f_T, o_w(x), B, c) = \frac{f_I(B + \beta \times (o_w(x) - B)) \cdot f_T(c)}{\|f_I(B + \beta \times (o_w(x) - B))\| \cdot \|f_T(c)\|}$$
   通过在基线图像到变换图像的路径上沿多条变换轨迹采样，BIG有效降低了采样点之间的梯度相似性（Figure 2揭示了传统集成梯度方法中采样点梯度相似性过高的问题），从而利用集成梯度的实现不变性减少对源模型的过度依赖。

### 文本模态攻击管线

文本模态的攻击管线独立运行，采用嵌入级别的扰动策略：首先评估每个词的重要性，然后在GloVe嵌入空间中进行近邻搜索，并结合掩码语言模型（MLM）预测生成语义相近的词替换候选，最终选择使攻击损失最大化的替换词。

### 模块间的协同关系

两个模态的攻击管线在损失函数层面实现协同——图像攻击和文本攻击共享同一个跨模态余弦相似度损失，使得生成的图像扰动和文本扰动能够协同作用，共同破坏视觉与语言之间的对齐关系。消融实验（Figure 4）证实，可学习变换（LT）和增强集成梯度（BIG）两个组件单独使用均可提高迁移性，而同时使用时攻击效果达到最优，验证了二者之间存在正向的协同效应。

### 补充图表

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed Transform to Transfer Attack: a multimodal framework for generating adversarial examples. For image modality, a learnable transformation strategy is applied to enhance input diversity and the boosted IG is adopted to generate visual adversarial examples. For text modality, we perform embedding-level perturbations to generate semantically superior word substitutions*

## 核心模块与公式推导

TTA 的核心由两个协同工作的图像攻击模块构成，分别解决输入多样性不足和源模型过拟合问题。

### 可学习图像变换模块

该模块的目标是为每张图像自适应地选择最优的块级变换组合，最大化输入多样性。其核心思想是：不同图像对变换操作的敏感性不同，固定的变换策略无法为所有图像提供最优的多样性增强。

**变换流程**：首先，维护两个列表——$M$ 种分块策略 $\{b_1, b_2, ..., b_m\}$ 和 $N$ 种变换操作 $\{t_1, t_2, ..., t_n\}$，并分别维护对应的概率分布 $P_b$ 和 $P_t$。对于输入图像 $x$，按以下步骤处理：

1. **分块**：根据概率分布 $P_b$ 采样分块策略 $b_i$，将图像划分为 $K$ 个图像块：
   $$b_i(x) = x^1 \oplus x^2 \oplus \cdots \oplus x^k$$

2. **块级变换**：对每个图像块 $x^k$，根据概率分布 $P_t$ 采样 $L$ 个变换操作并依次应用：
   $$t_L^k(x^k) = t_1^k \otimes t_2^k \otimes \cdots \otimes t_l^k$$

3. **整体变换**：将所有变换后的图像块重组为完整图像：
   $$o(x) = t_L^K(b_i(x)) = t_L^1(x^1) \oplus t_L^2(x^2) \oplus \cdots \oplus t_L^k(x^k)$$

概率分布 $P_b$ 和 $P_t$ 在攻击迭代过程中通过梯度反向传播进行优化，使得模型能够自适应地学习对当前图像最有效的变换组合。

### 增强集成梯度生成模块

该模块解决的核心问题是：传统集成梯度方法中，沿积分路径的采样点梯度相似度过高（如 Figure 2 所示），导致优化方向单一，对抗样本仍过度依赖源模型特征。

**BIG 公式**：增强集成梯度（Boosted Integrated Gradient, BIG）通过沿多条可学习变换路径采样来降低梯度相似性：
$$BIG_i(f_I, f_T, x, B, c) = (x_i - B_i) \times \sum_{w=1}^{Q_O} \frac{\partial \mathcal{L}(f_I, f_T, o_w(x), B, c)}{\partial x_i} \times \frac{1}{Q_O}$$

其中：
- $f_I, f_T$ 分别为图像编码器和文本编码器
- $x$ 为输入图像，$B$ 为基线图像（通常为全黑或全白图像）
- $c$ 为目标文本
- $o_w(x)$ 为第 $w$ 条可学习变换路径生成的变换变体
- $Q_O$ 为变换路径总数
- $(x_i - B_i)$ 为像素 $i$ 到基线的距离缩放因子

**损失函数**：计算变换后图像嵌入与目标文本嵌入的余弦相似度：
$$\mathcal{L}(f_I, f_T, o_w(x), B, c) = \frac{f_I(B + \beta \times (o_w(x) - B)) \cdot f_T(c)}{\|f_I(B + \beta \times (o_w(x) - B))\| \cdot \|f_T(c)\|}$$

其中 $\beta$ 为沿积分路径的插值系数。

### 文本攻击模块

文本模态的攻击采用嵌入空间扰动策略：结合词重要度评估定位关键 token，在 GloVe 嵌入空间中搜索语义相近的替换词，并利用掩码语言模型（MLM）预测结果筛选语义连贯的候选词，生成语义相近的文本对抗扰动。

### 模块协同机制

可学习变换模块为 BIG 提供多样化的变换路径 $o_w(x)$，BIG 沿这些路径采样计算梯度，利用集成梯度的实现不变性减少对源模型的过拟合。消融实验（Figure 4）表明，两个模块单独使用均可提升迁移性，但组合使用时攻击成功率最高，验证了二者的协同效应。

### 补充图表

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between other advanced attacks and our proposed method. (a), (b) and (c) illustrate the principal characteristics of SGA & LSSA, DRA and Ours, respectively. Meanwhile, (d) and (e) present a comparative analysis of the transfer capabilities demonstrated by these methods in image-text retrieval tasks. The multimodal adversarial examples are crafted on the ALBEF model to attack TCL, CLIPViT and*

## 实验与分析

### 主要实验结果

TTA在图像-文本检索任务上展现出显著的跨模型迁移攻击能力。Table 1报告了以不同VLP模型为源模型、跨架构攻击目标模型的攻击成功率（ASR）。在最具挑战性的**CLIP_CNN→ALBEF**迁移场景中，TTA的TRR@1达到55.16%，IRR@1达到66.42%，分别比此前最优方法**LSSA**（Liu et al., NAACL 2025）提升23.77和22.36个百分点。当源模型为ALBEF、目标模型为CLIP_ViT时，TTA的TRR@1和IRR@1分别高达92.27%和92.82%，在所有对比方法中取得压倒性优势。在源模型白盒设定下，TTA对ALBEF自身的TRR@1和IRR@1均达到100.00%，表明白盒攻击能力未因迁移性增强而受损。

跨任务迁移实验进一步验证了TTA攻击的泛化能力。Table 2展示了在MSCOCO图像描述任务上的结果：以ALBEF为源模型生成的对抗样本迁移至图像描述模型后，TTA在所有评估指标（BLEU-4、METEOR、ROUGE_L、CIDEr、SPICE）上均取得最低分数，其中BLEU-4降至12.1，显著低于原始数据的基线水平。这表明TTA生成的对抗扰动不仅跨模型迁移，还能有效跨任务迁移。

### 消融实验

Figure 4展示了可学习变换（Learnable Transformation, LT）与增强集成梯度（Boosted Integrated Gradient, BIG）两个核心组件的消融结果。单独引入LT或BIG均能提升跨模型迁移攻击成功率，而两者组合使用时达到最优效果。这一发现印证了方法设计的因果逻辑：LT通过自适应块级变换最大化输入多样性，BIG通过沿多条变换路径采样降低梯度相似性以缓解源模型过拟合，二者在机制上互补协同。

Table 3进一步在公平性条件下验证了TTA的优势。在控制增强图像数量相同的前提下，TTA仍显著优于**SGA**（Lu et al., ICCV 2023）和**DRA**（Gao et al., ECCV 2024）等方法，表明TTA的性能提升不仅来自变换数量的增加，更源于可学习变换选择策略本身的有效性。

### 攻击过程稳定性分析

Figure 7展示了不同攻击迭代步数下TTA攻击成功率的变化趋势。实验以ALBEF为源模型，在Flickr30K上生成对抗样本，报告对TCL、CLIP_ViT和CLIP_CNN三个目标模型的平均ASR。TTA在较少的攻击步数下即可快速收敛至高攻击成功率，且在整个攻击过程中保持稳定增长，未出现明显的过拟合退化现象。这得益于增强集成梯度的实现不变性特性，使攻击优化过程减少了对源模型特定梯度方向的过度依赖。

### 关键实验结论

综合实验结果，TTA的有效性建立在两个关键机制之上：

1. **可学习块级变换**：不同图像对变换操作的敏感性存在差异，固定变换策略无法适应这种异质性。TTA通过维护分块策略与变换操作的概率分布，在攻击过程中自适应选择最优变换组合，最大化输入多样性，从而生成更具泛化能力的对抗样本。

2. **增强集成梯度**：标准梯度计算高度依赖源模型的局部几何特性，导致对抗样本易过拟合至源模型。BIG沿多条变换路径采样并聚合梯度信息，利用集成梯度的实现不变性有效降低了梯度相似性（Figure 2可视化了传统方法中采样点梯度高度相似的问题），使生成的扰动方向更接近不同模型共享的决策边界特征。

在**CLIP_CNN→ALBEF**这一架构差异最大的迁移场景中，TTA相比LSSA提升超23个百分点，充分证明了上述机制在处理刁难迁移任务时的显著优势。

### 补充图表

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/004_Table_1.jpg]]
*Table 1: The attack success rate (%) of multimodal adversarial examples against different VLP models compared with state-of-the-art methods on image-text retrieval task. The source column represents the VLP models used for crafting multimodal adversarial examples on the Flickr30K dataset. The shaded area represents the white-box attacks*

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/005_Table_2.jpg]]
*Table 2: Results of cross-task transferability. The Baseline indicates the performance on original data; lower values denote better cross-task transferability of adversarial examples*

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/007_Figure_4.jpg]]
*Figure 4: Ablation Study: Attack Success Rate(%) on other three target models. We generate adversarial examples on ALBEF using the Flickr30K dataset to attack three target models: TCL*

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/009_Table_3.jpg]]
*Table 3: Comparison under the same number of augmented images. The shaded area represents the white-box attacks*

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/010_Figure_7.jpg]]
*Figure 7: Attack success rate in different attack processes. We generate adversarial examples on ALBEF for Flickr30K, where the reported ASR represents the average across three models: TCL*

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/008_Figure_5.jpg]]
*Figure 5: Attack success rates under different numbers of auxiliary transformed images QO*

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/006_Figure.jpg]]
*Figure: (a) ALBEF to TCL (b) ALBEF to CLIPViT (c) ALBEF to CLIPCNN*

![[assets/figures/papers/paper_list_l792_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Transform_to_Transf/figures/002_Figure_2.jpg]]
*Figure 2: The gradient similarity of sampling points along the integration path in SGA combined with integrated gradients. We craft adversarial examples on ALBEF for the Flickr30K dataset*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有视觉-语言预训练（VLP）模型的对抗攻击方法在提升跨模型迁移性时，面临两个结构性瓶颈：(1) 输入变换策略固定且有限，无法适应不同图像的敏感性差异；(2) 梯度优化过程高度依赖源模型，导致对抗样本过拟合于源模型的决策边界，迁移能力受限。**TTA** 的设计正是围绕这两个瓶颈展开，通过“可学习的块级变换”与“增强集成梯度”两个因果调节变量，系统性地提升迁移性。

### 与现有方法的关系

#### 输入变换策略的演进

在输入多样性增强这一维度上，现有方法呈现从“固定变换”到“学习选择”的演进脉络：

- **SGA**（Lu et al., ICCV 2023）采用 Set-level Guidance Attack，通过缩放变换增强样本多样性，但其变换操作是固定的，未考虑图像间的差异性。
- **LSSA**（Liu et al., NAACL 2025）引入局部洗牌和数据增强，同样受限于固定的变换策略集合。
- **DRA**（Gao et al., ECCV 2024）则从优化轨迹角度出发，通过对对抗轨迹的插值来缓解过拟合，但未触及输入变换的自适应选择问题。

**TTA** 在这一维度上的创新在于：将变换策略从“固定选择”升级为“可学习的块级组合”。具体而言，TTA 维护了两个概率分布——分块策略分布 $P_b$ 和变换操作分布 $P_t$，通过对每张图像自适应采样最优的分块方式与变换组合，最大化输入多样性。这一设计基于一个关键洞察：没有任何单一变换组合对所有图像都是最优的，且最有效的变换策略天然涉及块级操作。

#### 梯度计算方式的演进

在缓解源模型过拟合这一维度上，现有方法多采用标准梯度或简单的梯度平均：

- **PGD**（Madry et al., 2018）作为迭代投影梯度攻击基线，直接使用当前图像的梯度，迁移性有限。
- 将集成梯度（Integrated Gradient）与现有攻击结合的方法（如 SGA+IG）虽然引入了沿路径的梯度积分，但 **Figure 2** 的可视化揭示了一个关键问题：沿积分路径的采样点之间梯度相似性过高，导致集成梯度退化为近似标准梯度，未能有效降低对源模型的依赖。

**TTA** 提出的增强集成梯度（Boosted IG, BIG）通过在不同变换变体上分别计算梯度并加权聚合，打破了梯度相似性瓶颈。其核心公式为：

$$BIG_i(f_I, f_T, x, B, c) = (x_i - B_i) \times \sum_{w=1}^{Q_O} \frac{\partial \mathcal{L}(f_I, f_T, o_w(x), B, c)}{\partial x_i} \times \frac{1}{Q_O}$$

其中 $o_w(x)$ 表示第 $w$ 条变换路径下的图像变体，$B$ 为基线图像。通过在 $Q_O$ 条不同变换路径上采样，BIG 利用集成梯度的实现不变性（implementation invariance），显著降低了梯度相似性，从而减少了对源模型的过拟合。

#### 方法谱系定位

| 维度 | PGD | SGA / LSSA | DRA | TTA (本文) |
|------|-----|------------|-----|------------|
| 变换策略 | 无 | 固定、有限 | 无变换 | 可学习、块级、自适应 |
| 梯度计算 | 标准梯度 | 标准梯度 | 轨迹插值 | 增强集成梯度 (BIG) |
| 过拟合缓解 | 无 | 有限 | 轨迹层面 | 梯度+变换双重缓解 |

### 两个组件的协同机制

消融实验（**Figure 4**）明确表明：可学习变换（LT）和增强集成梯度（BIG）各自独立使用均可提升迁移性，但两者组合使用时达到最佳攻击效果。这一协同效应源于两个组件的互补性——LT 通过最大化输入多样性为 BIG 提供差异化的变换路径，而 BIG 通过在这些路径上采样降低梯度相似性，二者形成正向循环。

### 适用边界与局限

**已知适用场景：**
- 跨 VLP 架构迁移：从 ALBEF 到 CLIP_CNN/ViT、TCL 等不同架构均有效
- 跨任务迁移：在图像-文本检索上生成的对抗样本可迁移至图像描述（Image Captioning）和视觉定位（Visual Grounding）任务
- 多模态联合攻击：同时支持图像和文本模态的对抗扰动生成

**需要手动验证的局限：**
- 论文未提供 TTA 在面对对抗训练等防御策略时的有效性评估，该场景下的鲁棒性需要进一步验证
- 可学习变换模块引入了额外的计算开销，在大规模数据集上的可扩展性未被充分讨论
- 增强集成梯度中的变换路径数量 $Q_O$ 对攻击效果的敏感性分析（**Figure 5**）仅在有限范围内展开，极端取值下的行为未知

### 开放问题

1. **自适应攻击强度**：TTA 的可学习变换能否进一步与自适应攻击强度结合，根据目标模型的反馈动态调整变换策略？
2. **更多模态的泛化**：增强集成梯度在视频-语言、音频-语言等更多模态组合上的迁移性如何？变换操作池需要如何扩展？
3. **计算效率优化**：如何通过变换共享或梯度近似来降低 TTA 的计算开销，使其适用于更大规模的数据集和实时攻击场景？
4. **防御鲁棒性**：该方法在面对对抗训练、梯度掩蔽等防御策略时的有效性如何？是否需要针对防御策略进一步改进变换选择机制？

## 原文 PDF

![[paperPDFs/CVPR_2026/Transform_to_Transfer_Boosting_Adversarial_Attack_Transferability_on_Vision_Language_Pre_training_Models.pdf]]
