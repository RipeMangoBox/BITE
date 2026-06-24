---
title: "LATA: Laplacian-Assisted Transductive Adaptation for Conformal Uncertainty in Medical VLMs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LATA_Laplacian_Assisted_Transductive_Adaptation_for_Conformal_Uncertainty_in_Medical_VLMs.pdf
project_link: null
code_link: null
aliases:
- LLATA
- LATA
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: LATA在联合校准-测试池上构建图像间kNN图，以确定性、无标签、无训练的CCCP均值场平滑零样本概率，保证可交换性；同时引入基于ViLU的失败感知共形评分，利用实例级难度和标签可信度信号提升集合效率与类间公平。
primary_logic: 通过图拉普拉斯正则化在保持零样本保真度的前提下传播标签概率，使精炼的概率分布在平滑性和对原始分布的忠实性之间取得平衡，从而在不使用目标域标签和模型训练的条件下缩小预测集并降低类条件覆盖缺口，且可将校准边际先验以对称方式一次性注入来进一步收紧覆盖。
claims:
- 在16-shot校准设定下，LATA-LF（β=0）相较于最强无监督转导基线SCA-T，APS平均集合大小减少12%（3.35→2.95），CCV下降12%（7.18→6.32），同时维持名义覆盖率0.900。
- LATA-LF采用确定性对称变换，其覆盖率在不同随机种子下始终保持在名义水平附近，而使用同一校准集训练线性探针并共形化的Adapt+SCP因违反可交换性而系统性低于名义覆盖。
- 消融实验表明，仅图平滑（无ViLU）即可实现大部分效率增益（Size 3.05, CCV 6.60），而加入ViLU的难度u和注意力α可进一步降低CCV或缩小集合；校准边际先验β作为温和的调节旋钮，在β=0.3时将覆盖率提升至0.914，集合大小仅略增至3.20。
- Average over 9 medical adaptation tasks 上 Avg Set Size (APS, α=0.10) = 2.95 (LATA-LF, β=0)
---

# LATA: Laplacian-Assisted Transductive Adaptation for Conformal Uncertainty in Medical VLMs

> [!tip] 核心洞察
> 通过图拉普拉斯正则化在保持零样本保真度的前提下传播标签概率，使精炼的概率分布在平滑性和对原始分布的忠实性之间取得平衡，从而在不使用目标域标签和模型训练的条件下缩小预测集并降低类条件覆盖缺口，且可将校准边际先验以对称方式一次性注入来进一步收紧覆盖。

| 字段 | 内容 |
|------|------|
| 中文题名 | LATA：面向医学视觉-语言模型的拉普拉斯辅助转导自适应共形预测 |
| 英文题名 | LATA: Laplacian-Assisted Transductive Adaptation for Conformal Uncertainty in Medical VLMs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.17535) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | LATA (Laplacian-Assisted Transductive Adaptation) |
| Dataset | Average over 9 medical adaptation tasks |

> [!tip] 效果简介
> - Average over 9 medical adaptation tasks 上，Avg Set Size (APS, α=0.10) 2.95 (LATA-LF, β=0) vs 4.05 (SCP) (-1.10)；CCV (APS, α=0.10) 6.32 (LATA-LF) vs 9.59 (SCP) (-3.27)；Avg Set Size (LAC, α=0.10) 3.07 (LATA-LF) vs 3.30 (SCA-T) (-0.23)。

## 概述

在医学影像诊断中，零样本视觉-语言模型（VLM）为开放世界分类提供了无需领域微调的途径，但其共形预测集合在少量校准样本和类别严重不平衡的条件下面临两大瓶颈：**预测集过大**（低效率）与**类间覆盖率严重失衡**（高CCV）。直接利用校准标签进行自适应（如训练线性探针后共形化）会破坏样本可交换性，导致有限样本覆盖保证失效，使预测集系统性低于名义覆盖率。

LATA（Laplacian-Assisted Transductive Adaptation）针对上述瓶颈提出了一条**确定性、无标签、无训练**的转导精炼路径。其核心机制是在联合校准-测试池上构建图像间kNN图，通过CCCP均值场迭代平滑零样本概率分布，在保持对原始分布忠实度的前提下传播邻域一致性，从而在严格保留可交换性的条件下缩小预测集并降低类条件覆盖缺口。同时，LATA引入基于ViLU的**失败感知共形评分**，利用实例级难度和标签可信度信号进一步提升集合效率与类间公平性。可选地，校准边际先验可通过对称方式一次性注入，在几乎不增加集合大小的前提下收紧覆盖率。

在16-shot校准设定下，LATA的无标签变体（LATA-LF）相较于最强无监督转导基线**SCA-T**（Silva-Rodríguez et al., MICCAI 2025），APS平均集合大小减少12%（3.35→2.95），CCV下降12%（7.18→6.32），同时维持名义覆盖率0.900。消融实验表明，仅图平滑即可实现大部分效率增益，而ViLU的难度与注意力信号进一步压缩CCV或集合大小；校准边际先验作为温和调节旋钮，在β=0.3时将覆盖率提升至0.914而集合大小仅略增至3.20。可交换性验证显示，LATA-LF在不同随机种子下覆盖率始终稳定在名义水平附近，而使用同一校准集训练线性探针的Adapt+SCP则系统性低于名义覆盖，凸显了LATA确定性对称变换的有效性保障。

在方法谱系中，LATA定位于**转导式共形预测**的交叉地带：它区别于依赖标签训练适配器的全共形适应（FCA, Silva-Rodríguez et al., IPMI 2025）和基于熵最小化的无监督转导方法（SCA-T），也不同于通过最优传输对齐VLM logits的Conf-OT（Silva-Rodríguez et al., CVPR 2025）或梯度驱动的少样本转导学习（TIM, Boudiaf et al., NeurIPS 2020; TransCLIP, Zanella et al., NeurIPS 2024）。LATA的独特之处在于将图拉普拉斯正则化与共形预测的可交换性要求深度融合，以纯推理端的概率精炼实现覆盖-效率-公平的三重改进，为医学影像场景下有限标注的可靠决策提供了新的基线。

## 背景与动机

### 医学视觉-语言模型的零样本部署困境

视觉-语言模型（VLM）如 CLIP 及其医学领域特化变体，通过大规模图文预训练获得了强大的零样本识别能力，在无需目标域标注的条件下即可完成图像分类。这一特性对标注成本高昂、专家资源稀缺的医学影像场景极具吸引力。然而，零样本预测本质上缺乏统计可靠性保证：模型输出的概率分布未经校准，无法量化单个预测的不确定性，直接应用于临床决策存在显著风险。

共形预测（Conformal Prediction）提供了模型无关、分布无关的有限样本覆盖保证——给定用户指定的错误率 $\alpha$，预测集合以高概率包含真实标签。但标准的拆分共形预测（SCP）直接作用于零样本概率时，面临两个相互纠缠的瓶颈：

**瓶颈一：集合过大与类间覆盖失衡。** 在少量校准样本（如 16-shot）、类别高度不平衡的医学影像设定下，零样本概率分布通常较为平坦且存在系统性偏差，导致共形预测集合包含过多候选类别（平均集合大小可达 4.05），同时各类别的条件覆盖率严重偏离名义水平——高 CCV（Class-Conditioned Coverage Gap）值（如 9.59）意味着某些类别被系统性过度覆盖，而另一些则覆盖不足。这种不公平的覆盖模式在临床场景中尤为危险：罕见病类别可能被频繁排除在预测集之外。

**瓶颈二：直接利用校准标签会破坏可交换性。** 一个自然的改进思路是利用校准集的真实标签来调整预测概率——例如训练线性探针或适配器，然后再进行共形化。但这一做法违反了拆分共形预测的核心假设：校准样本与测试样本必须可交换。一旦校准集被用于模型训练或自适应，校准残差与测试残差不再服从同一分布，有限样本覆盖保证随即失效。实验证据表明，**Adapt+SCP**（在校准集上训练线性探针后共形化）在不同随机种子下系统性低于名义覆盖率，构成“覆盖不足陷阱”。

### 现有转导自适应的进展与缺口

为在不使用测试标签的前提下提升零样本预测质量，转导自适应（Transductive Adaptation）成为一条有前景的技术路线。其核心思想是：利用联合校准-测试池的无标签结构信息（如图像嵌入的几何关系）来精炼预测，同时保持对测试标签的不可见性。

现有方法可分为两类：

- **无监督转导方法**：如 **SCA-T**（Silva-Rodríguez et al., MICCAI 2025）通过熵最小化在联合池上优化置信度；**Conf-OT**（Silva-Rodríguez et al., CVPR 2025）利用最优传输对齐 VLM logits；**TransCLIP**（Zanella et al., NeurIPS 2024）采用无监督 GMM 进行转导适配。这些方法不接触校准标签，因此保留了可交换性，但优化过程依赖梯度更新或迭代对齐，计算开销较大，且效率提升有限——SCA-T 在 APS 得分下平均集合大小仅从 4.05 降至 3.35，CCV 从 9.59 降至 7.18。

- **标签感知转导方法**：如 **FCA**（Silva-Rodríguez et al., IPMI 2025）为每个类别训练独立适配器，在覆盖-效率前沿上表现最优，但需要在校准阶段使用真实标签，违背了无标签转导的初衷，且计算成本随类别数线性增长。

现有方法的共同缺口在于：缺乏一种**确定性、无训练、无标签**的转导精炼机制，能够在严格保持可交换性的同时，显著压缩预测集并缩小类间覆盖缺口。

### 失败感知评分的必要性

除了概率精炼，非一致性得分函数的设计同样影响共形预测的效率与公平性。标准得分（LAC、APS、RAPS）仅依赖概率排序，忽略了实例级难度差异：对于模型高度不确定的困难样本，理应付出更大的集合代价以维持覆盖；对于模型确信且正确的样本，应尽可能缩小集合。现有方法缺乏利用 VLM 内部表征来预测实例级失败风险的机制。

### 本文动机

针对上述瓶颈，本文提出 **LATA（Laplacian-Assisted Transductive Adaptation）**——一种拉普拉斯辅助的转导自适应框架，核心动机在于：

1. **以图结构传播替代梯度优化**：在联合校准-测试池上构建稀疏 kNN 图，通过图拉普拉斯正则化的 CCCP 均值场迭代平滑零样本概率。这一过程是确定性的、无需反向传播，天然保持校准与测试样本的可交换性。

2. **以失败感知评分提升效率与公平**：引入冻结的 ViLU（Vision-Language Uncertainty）模块，预测实例级失败概率和标签注意力，将其融入非一致性得分，使困难样本付出更高代价、可信样本缩小集合，从而在不牺牲覆盖的前提下进一步降低 CCV 和集合大小。

3. **以一次性标签先验温和收紧覆盖**：可选地将校准集类别边际分布以对称方式注入零样本概率，在不破坏可交换性的条件下，将覆盖提升至名义水平之上，仅以微小的集合增大为代价。

通过上述设计，LATA 旨在定义无标签转导共形预测的覆盖-效率最优前沿，逼近标签感知方法的性能，同时保持黑盒 VLM 的零样本部署优势与严格的有限样本覆盖保证。

## 核心创新

LATA 的核心创新并非修改视觉-语言模型的参数或引入目标域标签训练，而是围绕**共形预测框架下的两个关键“槽位”**——预测概率向量与非一致性得分函数——进行无标签、无训练的转导式精炼，在严格保持可交换性（从而维持有限样本覆盖保证）的前提下，同时提升预测集的效率与类间公平性。

### 创新槽位一：从零样本概率到图平滑精炼概率

**基线槽位值**：冻结 VLM 输出的原始零样本概率分布 $q(x)$（温度缩放 softmax，Eq. 1）。该分布在少量校准样本、类别严重不平衡的医学影像场景下，往往产生过大的预测集和显著的类条件覆盖缺口（CCV）。

**LATA 的替代方案**：在联合校准-测试池上构建稀疏 kNN 图，通过 CCCP 均值场迭代将 $q(x)$ 精炼为 $\tilde{z}(x)$（Eq. 5–6）。这一过程的本质是**图拉普拉斯正则化下的分布平滑**：最小化精炼分布与原始分布的 KL 散度（保真项），同时约束相邻样本的分布接近（平滑项），在平滑性与忠实性之间取得平衡。

**关键设计决策与因果机制**：

1. **确定性对称变换**：图平滑作用于整个联合池（校准+测试），对校准样本和测试样本施加完全相同的无标签变换。这与 Adapt+SCP（在校准集上训练线性探针后共形化）形成鲜明对比——后者破坏了校准集与测试集的可交换性，导致系统性覆盖不足（Figure 4b）。LATA 的对称设计是其在 16-shot 设定下维持名义覆盖率的结构性保障。

2. **无标签、无训练**：图构建仅依赖冻结的图像嵌入的余弦相似度（Eq. 5 中的 $W_{ij}^{\mathrm{g}}$），CCCP 更新仅涉及概率向量的乘法与归一化（Eq. 6），不涉及任何梯度反传或 VLM 权重更新。这使得 LATA 在推理时可作为轻量后处理模块嵌入任意黑盒 VLM。

3. **可选标签先验的对称注入**：LATA-LI 变体将校准集的类别边际 $m$ 以指数 $\beta$ 乘入零样本概率（Eq. 7），且**一次性、对称地**应用于校准和测试样本。这种设计将标签信息转化为温和的调节旋钮——消融实验表明，$\beta$ 从 0 增至 0.3，覆盖率从 0.900 提升至 0.914，集合大小仅从 3.07 略增至 3.20，CCV 从 6.40 降至 6.22（Table S6），验证了先验注入在效率-覆盖权衡中的可控性。

**证据强度**：消融实验（Table 3）直接量化了图平滑的独立贡献——仅图平滑（无 ViLU）在 $\alpha=0.10$ 下即可将平均集合大小从 SCP 的 4.05 降至 3.05，CCV 从 9.59 降至 6.60，已显著优于最强无监督转导基线 SCA-T（Size 3.30, CCV 7.47）。这表明**图平滑本身是效率增益的主要驱动因素**。

### 创新槽位二：从标准非一致性得分到失败感知得分

**基线槽位值**：标准 LAC/APS/RAPS 非一致性得分 $S_{\mathrm{base}}$（Eq. 9–11），仅依赖概率排序和随机扰动，不区分样本难度或标签可信度。

**LATA 的替代方案**：引入失败感知得分 $S^{\star}(x, y) = S_{\mathrm{base}}(\tilde{z}(x), y)(1 + \lambda u(x)) - \eta \alpha_y(x)$（Eq. 8），融合 ViLU 模块提供的两个信号：
- **实例级难度 $u(x)$**：ViLU 预测的失败概率，通过交叉注意力机制融合图像嵌入、预测类别文本嵌入和概率向量（Eq. 3）。$u(x)$ 作为乘性因子增大困难样本的非一致性得分，使其更可能被排除在预测集外，从而压缩集合大小。
- **标签注意力 $\alpha(x)$**：ViLU 输出的标签级可信度向量，$\alpha_y(x)$ 作为减性因子降低可信标签的得分，使其更容易被纳入预测集，从而提升覆盖率。

**关键设计决策**：
- ViLU 模块在源域预训练后**冻结**，推理时仅执行前向传播，不参与图平滑或 VLM 更新。这保持了 LATA 整体的无训练特性。
- $\lambda$ 和 $\eta$ 控制两个信号的强度，可通过网格搜索在保持覆盖率的约束下优化效率（Table S2 给出了敏感性分析）。

**证据强度**：组件消融（Table 3）表明，在图平滑基础上加入 ViLU 的难度信号 $u$ 和注意力信号 $\alpha$，可进一步将 CCV 从 6.60 降至 6.40（集合大小 2.95），或将集合大小从 3.05 进一步压缩。ViLU 的增益虽小于图平滑的主体贡献，但在类间公平性维度上提供了可观的边际改进。

### 方法谱系与知识库定位

LATA 处于**转导式共形预测**与**图半监督学习**的交叉点。与现有工作的关系如下：

- **SCP（Vanilla Split Conformal）**：仅使用原始零样本概率和标准得分，无任何适应。LATA 在保持其覆盖保证的前提下大幅改进效率与公平性。
- **SCA-T**（Silva-Rodríguez et al., MICCAI 2025）：通过熵最小化进行无监督转导适应，但需要梯度优化且未显式建模类间覆盖平衡。LATA 以确定性图平滑替代优化，在效率和 CCV 上均优于 SCA-T（Table 1：APS Size 2.95 vs. 3.35，CCV 6.32 vs. 7.18）。
- **Conf-OT**（Silva-Rodríguez et al., CVPR 2025）：基于最优传输的 logit 适应，同样涉及优化。LATA 的图平滑提供了更轻量的替代方案。
- **FCA**（Silva-Rodríguez et al., IPMI 2025）：全共形适应，使用目标域标签训练 per-label 适配器，是标签感知的 oracle 方法。LATA-LI 在无目标域标签的条件下，性能已接近 FCA（PAPY 数据集 APS：LATA-LI 覆盖率 0.910, Size 3.03, CCV 6.25 vs. FCA 覆盖率 0.898, Size 3.06, CCV 6.12），表明对称标签先验注入是缩小与标签方法差距的有效手段。
- **TIM**（Boudiaf et al., NeurIPS 2020）与 **TransCLIP**（Zanella et al., NeurIPS 2024）：基于梯度的转导少样本学习方法，需优化模型参数。LATA 的无训练特性在医学场景中更具部署优势。
- **Adapt+SCP**：作为负对照，在校准标签上训练线性探针后共形化，因违反可交换性而系统性低于名义覆盖（Figure 4b），反衬出 LATA 对称设计的关键性。

### 边界与局限

1. **任务范围受限**：当前设计仅针对图像分类的共形预测，未扩展到密集预测、分割或多标签等结构化输出任务——这些场景下图构建和得分函数设计需要根本性重构。
2. **图结构的鲁棒性**：图构建依赖图像嵌入的 kNN 近似，当标签空间极大（>10k 类）或分布偏移剧烈时，kNN 图可能无法准确捕捉语义邻近关系，先验注入的有效性也会受限于校准边际估计的不确定性。
3. **ViLU 的黑盒依赖**：失败预测模块需要源域预训练数据，虽推理时冻结，但其预测质量依赖于源域与目标域的分布相似性，在严重域偏移下的行为尚未充分验证。
4. **极度小样本下的先验不确定性**：LATA-LI 的标签先验来自校准集类别边际，当每类仅 1–2 个样本时，边际估计的方差可能显著影响性能——Table S6 中 β 的最优值可能随样本量漂移，需要手动验证。

## 整体框架

LATA的整体流水线围绕一个核心设计原则展开：**在严格保持共形预测可交换性（exchangeability）的前提下，通过无标签、无训练的图转导精炼来提升零样本视觉-语言模型（VLM）的预测集效率与类间公平性**。流水线由五个顺序模块构成，信息流从冻结的VLM前向传播开始，经图平滑与失败感知评分，最终输出具有覆盖率保证的共形预测集合。

### 模块关系与信息流

1. **零样本概率计算**：给定输入图像 $x$，冻结的视觉编码器提取图像嵌入 $v$，文本编码器为 $C$ 个类别生成文本嵌入 $\{w_c\}_{c=1}^C$。通过温度缩放softmax得到初始类别分布 $q(x) \in \Delta^{C-1}$（见 Eq. (1)）。该模块是整个流水线的起点，所有后续精炼均以此分布为基础。

2. **ViLU失败预测头**：一个预训练但推理时冻结的交叉注意力模块，接收VLM的视觉-文本特征，输出实例级失败概率 $u(x)$ 和标签注意力向量 $\alpha(x)$。ViLU不参与VLM权重的任何更新，仅提供难度与标签可信度信号，供后续非一致性评分使用。

3. **LATA图平滑（核心精炼模块）**：在联合校准-测试池上构建稀疏kNN图，以图像嵌入的余弦相似度定义边权重。通过少量CCCP均值场迭代更新，将零样本概率 $q(x)$ 精炼为平滑后的分布 $\tilde{z}(x)$。该过程**确定性、对称地作用于校准与测试样本**，不接触任何标签信息，从而严格保持可交换性。可选地，LATA-LI变体在平滑前将校准集类别边际先验 $m$ 以指数 $\beta$ 一次性、对称地注入 $q(x)$，为覆盖率提供温和的调节旋钮。

4. **失败感知非一致性评分**：将平滑后的概率 $\tilde{z}(x)$ 与ViLU输出融合，构建失败感知得分 $S^\star(x, y) = S_{\mathrm{base}}(\tilde{z}(x), y)(1 + \lambda u(x)) - \eta \alpha_y(x)$（见 Eq. (8)）。基础得分 $S_{\mathrm{base}}$ 可选LAC、APS或RAPS，分别对应不同的集合构造策略。

5. **共形预测集构造**：利用校准集上的 $S^\star$ 分数计算经验 $(1-\alpha)$ 分位数阈值 $\hat{s}$，对测试样本将所有满足 $S^\star(x, y) \le \hat{s}$ 的类别 $y$ 纳入预测集 $\mathcal{C}(x)$。该步骤继承标准分裂共形预测的有限样本覆盖率保证。

### 关键设计选择

- **可交换性保持**：LATA-LF通过确定性对称变换作用于校准与测试样本，严格保持可交换性，从而保留SCP的有限样本覆盖率保证。LATA-LI的一次性标签先验同样对称应用，不影响有效性。两种变体均未在转移时接触测试标签，避免了Adapt+SCP等方法的覆盖不足陷阱（见 Figure 4(b)）。
- **无训练、无标签转导**：整个精炼过程不更新VLM参数，不使用测试域标签。LATA-LF完全无标签；LATA-LI仅在校准阶段一次性使用校准标签边际，不破坏可交换性。
- **模块化组合**：图平滑与ViLU可独立启用或禁用。消融实验表明，仅图平滑（无ViLU）即可实现大部分效率增益（集合大小3.05，CCV 6.60），加入ViLU的难度 $u$ 和注意力 $\alpha$ 可进一步降低CCV或缩小集合（见 Table 3）。校准边际先验 $\beta$ 作为温和的调节旋钮，在 $\beta=0.3$ 时将覆盖率提升至0.914，集合大小仅略增至3.20（见 Table S6）。

### 输入输出规范

| 模块 | 输入 | 输出 |
|------|------|------|
| 零样本概率计算 | 图像 $x$，类别文本提示 | $q(x) \in \Delta^{C-1}$ |
| ViLU失败预测头 | VLM视觉-文本特征 | $u(x) \in [0,1]$，$\alpha(x) \in \mathbb{R}^C$ |
| LATA图平滑 | $q(x)$，kNN图，可选先验 $m$ | $\tilde{z}(x) \in \Delta^{C-1}$ |
| 失败感知评分 | $\tilde{z}(x)$，$u(x)$，$\alpha(x)$，真实标签 $y$ | $S^\star(x, y) \in \mathbb{R}$ |
| 共形预测集构造 | 校准集 $\{S^\star(x_i, y_i)\}_{i=1}^{n_{\text{cal}}}$，目标误差率 $\alpha$ | 预测集 $\mathcal{C}(x_{\text{test}})$ |

Figure 1(a) 直观展示了上述流水线的完整信息流，Figure 1(b) 则给出了覆盖-效率前沿，表明LATA-LF在维持SCP级覆盖率的同时实现了更小的集合与更低的类条件覆盖缺口（CCV），LATA-LI以极小的效率代价进一步提升覆盖率。

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/001_Figure_1.jpg]]
*Figure 1: LATA pipeline and coverage–efficiency trade-off. (a) LATA pipeline. Frozen vision/text encoders yield zero-shot scores q(x), optionally adjusted via calibration-informed priors. LATA then refines predictions on the joint unlabeled pool U using a sparse kNN graph and CCCP updates, producing z˜(x). A frozen ViLU module estimates difficulty u(x) and attention α(x), forming a failure-aware score S⋆, which is conformalized into calibrated prediction sets. (b) Coverage–efficiency frontier (α=0.10, APS). LATA-LF (β=0) achieves SCP-level coverage with lower set size and CCV. LATA-LI (β=0.2) improves coverage further with minimal cost, outperforming SCA-T in both efficiency and balance*

## 核心模块与公式推导

LATA 的核心架构由五个冻结模块串联而成：零样本概率计算、ViLU 失败预测头、图拉普拉斯平滑、失败感知非一致性评分和共形预测集构建。整个流水线不更新视觉-语言模型的任何权重，仅在联合校准-测试池上执行确定性输出精炼。

### 零样本概率计算

给定冻结的视觉编码器输出的图像嵌入 $v \in \mathbb{R}^d$ 和文本编码器为 $C$ 个类别生成的文本嵌入 $\{w_c\}_{c=1}^C$，零样本类别概率通过温度缩放 softmax 获得：

$$p_c(W, v) := \frac{\exp(v^\top w_c / \tau)}{\sum_{j=1}^C \exp(v^\top w_j / \tau)}, \qquad p(W, v) \in \Delta^{C-1}$$

其中 $\tau$ 为温度参数，$\Delta^{C-1}$ 表示 $C$ 维概率单纯形。该分布 $q(x) = p(W, v)$ 构成后续所有精炼步骤的基分布。

### ViLU 失败预测头

ViLU（Failure Prediction Head）是一个冻结的轻量模块，通过交叉注意力机制预测每个样本的实例级失败概率 $u(x) \in [0,1]$ 和标签注意力向量 $\alpha(x) \in \mathbb{R}^C$。其输入为图像嵌入 $v$、零样本预测标签的文本嵌入 $t_{\hat{c}(x)}$ 以及零样本概率向量 $z_t^\alpha(x)$，通过一个小型 MLP 和 sigmoid 激活输出：

$$u(x) = \sigma(g([v, t_{\hat{c}(x)}, z_t^\alpha(x)]))$$

ViLU 在源域数据上预训练后完全冻结，推理时不参与任何更新，作为黑盒难度估计器为后续非一致性评分提供信号。

### LATA 图拉普拉斯平滑

这是方法的核心创新。在联合校准-测试池 $\mathcal{U}$（共 $N$ 个样本）上，基于归一化图像嵌入 $\tilde{v}_i$ 构建稀疏 kNN 图，边权重定义为：

$$W_{ij}^{\mathrm{g}} = \begin{cases} \exp(-\|\tilde{v}_i - \tilde{v}_j\|_2^2 / \sigma^2), & \text{if } i \sim j \\ 0, & \text{otherwise} \end{cases}$$

精炼目标是最小化保真项与图平滑项的加权组合：

$$\min_{\{\tilde{z}_i \in \Delta^{C-1}\}} \sum_{i=1}^{N} \mathrm{KL}(\tilde{z}_i \| q_i) + \frac{\gamma}{2} \sum_{i,j} W_{ij}^{\mathrm{g}} \|\tilde{z}_i - \tilde{z}_j\|_2^2$$

其中 $\gamma$ 控制平滑强度。该目标通过 CCCP 均值场迭代求解，更新规则为：

$$\tilde{z}_{ik}^{(t+1)} \propto q_{ik} \exp\Bigl(\gamma \sum_j W_{ij}^{\mathrm{g}} \tilde{z}_{jk}^{(t)}\Bigr), \qquad \sum_{k=1}^{C} \tilde{z}_{ik}^{(t+1)} = 1$$

每次迭代将当前邻居概率分布作为指数族消息乘入基分布，再重新归一化。默认迭代次数 $T_{\text{iter}}=8$，在速度与可靠性间取得平衡（降至 4 次可加速约 25%，对集合大小和 CCV 的影响轻微）。

**标签通知先验（LATA-LI）**：对于 $\beta > 0$，可利用校准集的类别边际分布 $m \in \Delta^{C-1}$ 一次性调整基分布：

$$q_{ik} \gets \frac{q_{ik} m_k^{\beta}}{\sum_{\ell=1}^C q_{i\ell} m_\ell^{\beta}}$$

该操作对称地应用于校准和测试样本，严格保持可交换性，因此不破坏有限样本覆盖保证。$\beta$ 作为温和的调节旋钮，在 $\beta=0.3$ 时可将覆盖率从 0.900 提升至 0.914，集合大小仅从 3.07 增至 3.20。

### 失败感知非一致性评分

将图平滑后的精炼概率 $\tilde{z}(x)$ 与 ViLU 信号融合，构造失败感知非一致性得分：

$$S^{\star}(x, y) = S_{\mathrm{base}}(\tilde{z}(x), y) \bigl(1 + \lambda u(x) \bigr) - \eta \alpha_y(x)$$

其中 $S_{\mathrm{base}}$ 可选用标准 LAC、APS 或 RAPS 得分，$u(x)$ 为实例级难度，$\alpha_y(x)$ 为真实标签 $y$ 的注意力权重。超参数 $\lambda, \eta \geq 0$ 控制各信号的贡献。该设计使困难样本（$u(x)$ 高）的非一致性得分放大，从而需要更大的预测集来覆盖；同时可信标签（$\alpha_y(x)$ 高）的得分被压低，有助于缩小集合。

三种基础得分的定义如下：

- **LAC**（最小歧义分类器）：$S_{\mathrm{LAC}}(x, y) = 1 - z_y(x)$
- **APS**（自适应预测集）：$S_{\mathrm{APS}}(x, y) = \sum_{j: \mathrm{rank}_x(j) < \mathrm{rank}_x(y)} z_j(x) + U \cdot z_y(x)$，其中 $U \sim \text{Uniform}(0,1)$
- **RAPS**（带正则化的自适应预测集）：$S_{\mathrm{RAPS}}(x, y) = \sum_{j: \mathrm{rank}_x(j) < \mathrm{rank}_x(y)} z_j(x) + \gamma_{\mathrm{raps}} \cdot \max\{0, \mathrm{rank}_x(y) - k_{\mathrm{reg}}\} + U \cdot z_y(x)$

### 共形预测集构建

利用校准集 $\mathcal{D}_{\text{cal}}$ 上计算的失败感知得分 $\{S^{\star}(x_i, y_i)\}_{i=1}^{n}$，取经验 $(1-\alpha)$ 分位数作为阈值：

$$\hat{s} = \inf\left\{ s : \frac{1}{n} \left| \{ i : s_i \leq s \} \right| \geq \frac{\lceil (n+1)(1-\alpha) \rceil}{n} \right\}$$

对测试样本 $x_{\text{test}}$，预测集为所有得分不超过阈值的类别集合：

$$\mathcal{C}(x_{\text{test}}) = \{ y : S^{\star}(x_{\text{test}}, y) \leq \hat{s} \}$$

整个过程保持确定性对称变换，确保可交换性条件成立，从而继承标准分裂共形预测的有限样本覆盖率保证：$P(y_{\text{test}} \in \mathcal{C}(x_{\text{test}})) \geq 1-\alpha$。

## 实验与分析

### 核心瓶颈与评估逻辑

医学视觉-语言模型在零样本共形预测中面临双重困境：**集合过大**与**类间覆盖率严重失衡**。在16-shot校准、类别不平衡的医学影像设定下，标准分裂共形预测（SCP）的平均预测集大小达4.05（APS，α=0.10），类条件覆盖缺口（CCV）高达9.59（Table 1）。直接利用校准标签进行自适应（如Adapt+SCP）会破坏可交换性，导致有限样本覆盖保证失效——这正是Figure 4(b)所揭示的关键陷阱：线性探针在相同校准集上训练并共形化后，覆盖率系统性低于名义水平，而LATA的确定性对称变换则始终维持有效覆盖。

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/002_Table_1.jpg]]
*Table 1: Conformal prediction results with 16-shot calibration across three nonconformity scores and two error levels*

LATA的实验评估围绕三个核心维度展开：**效率**（平均集合大小）、**公平性**（CCV）与**覆盖率保真度**（是否达到或超过名义覆盖率1-α）。以下分析基于9个医学适应任务的平均结果，涵盖三种非一致性得分（LAC、APS、RAPS）和两个错误水平（α∈{0.05, 0.10}）。

### 主实验结果：效率与公平的双重突破

**Table 1** 汇总了16-shot校准设定下的核心对比。LATA-LF（β=0，无标签先验变体）在所有无监督转导基线中表现最优：

- **效率增益**：在APS得分下，LATA-LF将平均集合大小从SCP的4.05降至2.95（-27%），相较于最强无监督转导基线SCA-T的3.35进一步缩减12%。在LAC得分下，集合大小从SCP的3.94降至3.07，优于SCA-T的3.30。
- **公平性提升**：CCV从SCP的9.59骤降至6.32（APS），相对SCA-T的7.18下降12%。LAC得分下CCV从9.05降至6.40（SCA-T为7.47）。
- **覆盖率维持**：LATA-LF在所有设定下均达到或超过名义覆盖率0.900，无红色违规标记。LATA-LI（β=0.2）通过一次性校准边际先验将覆盖率进一步提升至0.910（APS），集合大小仅微增至3.03，CCV进一步降至6.25。

在SICAPv2数据集的细粒度分析（Figure 2）中，LATA定义了最佳无标签效率前沿：随着校准样本数K从4增至16，LATA始终以更小的集合实现相等或更优的覆盖率，逼近使用标签的FCA方法（覆盖率0.898，集合大小3.06，CCV 6.12），但**在转移阶段完全不接触目标域标签**。测试时覆盖率分布显示，SCP和SCA-T虽减少违规但较为分散，而LATA的覆盖率紧密聚集在名义水平附近，CCV最低。

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/003_Figure_2.jpg]]
*Figure 2: SICAPv2 — coverage, efficiency, and set structure*

### 组件消融：图平滑是效率增益的主要驱动力

**Table 3** 的系统消融揭示了各组件的贡献权重：

- **纯图平滑（无ViLU）**：在α=0.10下，仅LATA图精炼（λ=η=0）即可将集合大小从SCP的3.94降至3.05，CCV从9.05降至6.60。这表明**图拉普拉斯正则化本身贡献了大部分效率增益**，通过在图结构上传播概率分布，使预测分布在保持零样本保真度的同时更加平滑。
- **ViLU难度信号u**：在LATA基础上引入失败概率u（λ>0, η=0），CCV进一步从6.60降至6.40，集合大小从3.05降至2.95。难度感知得分提高了困难样本的代价，使预测集更具判别性。
- **ViLU注意力信号α**：同时启用u和α（λ>0, η>0）在APS得分下进一步压缩集合大小，验证了标签级可信度信号对集合精炼的增益。
- **APS得分下的消融**（Table S5）呈现一致趋势，确认了组件贡献的跨得分鲁棒性。

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/011_Table_S.5.jpg]]
*Table S.5: Component ablation (APS) at*

### 标签先验的温和调控

校准边际先验β作为LATA-LI的核心调控旋钮，表现出**可控的覆盖-效率权衡**（Table S6）。在LAC得分α=0.10下：
- β=0：覆盖率0.900，集合大小3.07，CCV 6.40
- β=0.1：覆盖率0.907，集合大小3.11，CCV 6.31
- β=0.2：覆盖率0.910，集合大小3.14，CCV 6.28
- β=0.3：覆盖率0.914，集合大小3.20，CCV 6.22

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/015_Table_S.6.jpg]]
*Table S.6: Sensitivity to the label-informed prior (β). We apply the prior as*

β从0增至0.3时，覆盖率提升1.4个百分点，集合大小仅增加4.2%，CCV持续下降。这种**一次性、对称应用**的标签先验在不破坏可交换性的前提下，为覆盖不足的高风险场景提供了温和的校正机制。

### 转导求解器对比

**Table 2** 将LATA的CCCP均值场求解器与其他转导范式对比。基于梯度的TIM和基于GMM的TransCLIP在部分任务上出现覆盖率违规，且效率与公平性均不及LATA。Conf-OT虽在部分设定下接近LATA，但计算开销更高且缺乏ViLU的失败感知能力。CCCP迭代的收敛特性在Figure S1中得到验证：T_iter=8在速度与可靠性间取得平衡，降至4可加速约25%，对集合大小和CCV的影响轻微（APS: Size +0.08, CCV +0.05）。

### 超参数鲁棒性与样本效率

LATA对关键超参数表现出良好的鲁棒性：
- **图权重γ**（Table S3）：在0.1至1.0范围内，LATA-LF始终维持接近名义覆盖，集合大小和CCV明显优于SCP和SCA-T。
- **邻居数k**（Table S4）：在10至30范围内，性能波动很小，均显著优于基线。
- **校准样本数K**（Figure 3a）：从4-shot到16-shot，LATA在所有K值下均以更小集合和更低CCV优于SCA-T和SCP，且在极低样本条件下优势更为突出。
- **查询窗口大小W**（Figure 3b）：从64到全批量，LATA的性能稳定，表明图构建对批量大小不敏感，适合在线部署场景。

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/009_Table_S.3.jpg]]
*Table S.3: Sensitivity to Laplacian weight γ (APS, α=0.10, LATA-LF). All settings stay near nominal coverage and retain clear gains in Size/CCV vs. SCP (Size = 4.05, CCV = 9.59) and SCA-T*

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/012_Table_S.4.jpg]]
*Table S.4: Sensitivity to graph degree k (APS, α=0.10, LATA-LF). All settings remain near nominal coverage and maintain clear gains over SCP (Size = 4.05, CCV = 9.59) and SCA-T*

### 可交换性验证与效率增益归因

**Figure 4(b)** 的可交换性检验是关键证据：Adapt+SCP（线性探针训练与共形化使用相同校准集）在不同随机种子下系统性低于名义覆盖，验证了违反可交换性的严重后果。而LATA-LF的确定性、无标签变换作用于校准与测试的共享图结构，覆盖率在不同种子下始终保持在名义水平附近。

**Figure 4(a)** 进一步表明，LATA-LI相对于SCP的效率增益（ΔSet Size < 0）与准确率提升（ΔAccuracy > 0）之间仅存在弱线性关系（R²较小），说明**效率改进并非简单来自准确率提高**，而是图平滑和失败感知得分的独立贡献。

### 失败模式与局限性

尽管LATA在医学影像分类共形预测中表现突出，仍需注意以下边界：
1. **极端类别不平衡**：当校准边际先验的估计不确定性较高时（如某些类别仅有1-2个样本），β的调控效果可能受限，需手动验证先验质量。
2. **分布偏移剧烈场景**：图构建依赖图像嵌入的kNN近似，当目标域与源域分布差异极大时，图结构可能无法准确捕捉样本间语义关系，导致平滑效果下降。
3. **ViLU预训练依赖**：ViLU需要源域数据预训练（Table S8），虽然在推理时冻结且不参与VLM更新，但其失败预测质量受预训练数据覆盖范围影响。
4. **任务范围限制**：当前设计仅针对图像分类，未扩展到密集预测、分割或多标签等结构化输出任务，在这些场景下共形覆盖保证的维持需要新的方法论。

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/016_Table_S.8.jpg]]
*Table S.8: Effect of ViLU pretraining source (LAC, α=0.10). UT window: N=256, k=15*

### 补充图表

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/005_Table_2.jpg]]
*Table 2: Transductive solvers at α=0.10. Best and second-best results are shown in bold and underline, respectively. Red indicates violations of the target error rate*

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/006_Figure_4.jpg]]
*Figure 4: Exchangeability and per-dataset ∆accuracy–∆setsize (APS, α=0.10). (a) Across datasets, LATA-LI yields ∆Accuracy>0 and ∆Set Size\<0 vs. SCP, with a weak linear fit (small*

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/007_Table_3.jpg]]
*Table 3: Component ablations (LAC) at*

![[assets/figures/papers/paper_list_l2105_https_arxiv_org_abs_2602_17535/figures/010_Table_S.2.jpg]]
*Table S.2: Sensitivity to failure-aware weights*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

在少量样本、类别不平衡的医学影像设定下，零样本视觉-语言模型（VLM）的共形预测面临双重困境：预测集合通常过大（效率低下），且类间覆盖率严重失衡（高CCV）。直接利用校准标签进行自适应（如训练线性探针后共形化，即Adapt+SCP）会破坏校准集与测试集之间的可交换性，使有限样本覆盖保证失效。LATA的设计正是围绕这一瓶颈展开：在**不接触VLM权重、不使用目标域标签进行训练**的前提下，通过确定性转导精炼缩小预测集并降低类条件覆盖缺口。

### 方法谱系中的定位

LATA处于**无监督转导共形预测**（unsupervised transductive conformal prediction）这一新兴方法线上，与以下工作形成直接对比：

- **SCP**（Vanilla Split Conformal）：零样本共形预测基线，不做任何适应，直接使用原始VLM概率计算非一致性得分并构造预测集。效率最低（APS平均集合大小4.05），CCV最高（9.59），代表性能下界。
- **SCA-T**（Silva-Rodríguez et al., MICCAI 2025）：无监督转导适应方法，在联合校准-测试池上通过熵最小化优化VLM输出分布。LATA-LF（β=0）相较于SCA-T，APS平均集合大小减少12%（3.35→2.95），CCV下降12%（7.18→6.32），同时维持名义覆盖率0.900（Table 1）。
- **Conf-OT**（Silva-Rodríguez et al., CVPR 2025）：基于最优传输的VLM logit转导适应。LATA在图转导求解器对比中表现更优（Table 2）。
- **FCA**（Silva-Rodríguez et al., IPMI 2025）：全共形适应（标签感知oracle），使用逐类适配器，代表性能上界。LATA-LI（β=0.2）在PAPY数据集上达到覆盖率0.910、集合大小3.03、CCV 6.25，已接近FCA（覆盖率0.898、集合大小3.06、CCV 6.12），而**完全不使用目标域标签进行适应**（Figure 2, Section 4.2）。
- **TIM**（Boudiaf et al., NeurIPS 2020）与**TransCLIP**（Zanella et al., NeurIPS 2024）：基于梯度的转导小样本学习和无监督GMM转导适应。LATA在图转导求解器对比中展现出更优的效率-公平性权衡（Table 2）。
- **Adapt+SCP**：负面对照——在校准标签上训练线性探针后包裹SCP。因违反可交换性，其覆盖率在不同随机种子下系统性低于名义水平，而LATA-LF的覆盖率始终保持在名义水平附近（Figure 4(b), Section 4.3）。

### 关键设计选择与适用边界

LATA的核心技术路线由三个相互协同的模块构成，每个模块都体现了特定的设计取舍：

1. **图转导精炼（LATA Graph Smoothing）**：在联合校准-测试池上构建稀疏kNN图，通过CCCP均值场迭代（$T_{\text{iter}}=8$）平滑零样本概率。该过程是**确定性、无标签、无训练**的对称变换，严格保持可交换性。消融实验表明，仅图平滑（无ViLU）即可实现大部分效率增益（集合大小3.05，CCV 6.60），而SCP为4.05/9.59（Table 3）。

2. **失败感知共形评分（ViLU + Failure-Aware Scoring）**：ViLU通过交叉注意力预测实例级失败概率$u(x)$和标签注意力向量$\alpha(x)$，融合为基础得分的修正项$S^{*}(x,y) = S_{\text{base}}(\tilde{z}(x), y)(1 + \lambda u(x)) - \eta \alpha_y(x)$。加入$u$和$\alpha$后，CCV进一步从6.60降至6.40，集合大小从3.05降至2.95（Table 3）。

3. **标签通知先验（Label-Informed Prior）**：将校准类别边际$m$以$\beta$指数乘入零样本概率，一次性、对称地应用于校准与测试样本。$\beta$作为温和的调节旋钮，在$\beta=0.3$时将覆盖率从0.900提升至0.914，集合大小仅从3.07增至3.20，CCV从6.40降至6.22（Table S6）。

**适用边界**：目前LATA仅针对图像分类任务设计，未扩展到密集预测、分割或多标签等结构化输出。图构建依赖图像嵌入的kNN近似，当标签空间极大（>10k类）或分布偏移剧烈时，图结构和先验可能不够鲁棒。ViLU失败预测模块需要预训练的源域数据，推理时冻结且不参与VLM更新，仍属黑盒模块。

### 局限与开放问题

**已识别的局限**：
- 任务范围限于图像分类，未涉及密集预测或多标签场景。
- 图构建对分布偏移敏感，极端不平衡条件下先验估计的不确定性可能影响性能。
- ViLU模块依赖源域预训练，增加了方法部署的外部依赖。

**开放问题**：
- 如何将图转导精炼扩展到密集预测、分割或多标签任务，同时保持共形覆盖保证？
- 在处理大规模标签空间（>10k类）时，是否可结合近似图构建与降维策略以维持计算效率？
- 能否设计自适应先验强度或更复杂的图结构（如动态邻居、异构边）以应对更强的分布偏移？
- 是否存在更有效的标签先验注入方式，在不牺牲有效性的前提下进一步优化覆盖与效率的权衡？

## 原文 PDF

![[paperPDFs/CVPR_2026/LATA_Laplacian_Assisted_Transductive_Adaptation_for_Conformal_Uncertainty_in_Medical_VLMs.pdf]]
