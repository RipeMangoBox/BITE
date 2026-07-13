---
title: "ACE: Attribution-Controlled Knowledge Editing for Multi-hop Factual Recall"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ACE_Attribution_Controlled_Knowledge_Editing_for_Multi_hop_Factual_Recall.pdf
project_link: null
code_link: null
aliases:
- AACKE
- ACE
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/interpretability_and_visualization
core_operator: "**查询-值神经通路**：在多跳推理中，隐式主语充当查询神经元，依次激活各层的值神经元以累积信息；编辑这些关键通路（尤其是深层值神经元和中级查询神经元）即可恢复正确的多跳推理。"
primary_logic: "大型语言模型通过依次执行\"查询-值\"相互作用来积累信息：查询神经元（由隐式主语触发）顺序激活相关的值神经元，逐步将证据汇聚到最终答案。因此，知识编辑不仅要更新存储事实的值神经元，还需调整激活这些值神经元的查询神经元，以保障多跳推理链的通畅。"
claims:
- "ACE在GPT-J上的多跳准确率比最强基线PMET提高9.44%，在Qwen3-8B上提高37.46%。"
- "对前1%的语义相关神经元进行因果干预导致准确率下降超过90%，而随机干预下降不到10%。"
- "消融实验表明：略过查询层导致准确率下降16.51%，而略过值层导致准确率骤降40.45%。"
- "MQuAKE-3K 上 多跳准确率 (Average Accuracy %) = ACE: 46.45 (GPT-J), 58.24 (Qwen3-8B)"
---

# ACE: Attribution-Controlled Knowledge Editing for Multi-hop Factual Recall

> [!tip] 核心洞察
> 大型语言模型通过依次执行"查询-值"相互作用来积累信息：查询神经元（由隐式主语触发）顺序激活相关的值神经元，逐步将证据汇聚到最终答案。因此，知识编辑不仅要更新存储事实的值神经元，还需调整激活这些值神经元的查询神经元，以保障多跳推理链的通畅。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ACE：基于归因控制的多跳事实回忆知识编辑 |
| 英文题名 | ACE: Attribution-Controlled Knowledge Editing for Multi-hop Factual Recall |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IuWIzmMvKo) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/interpretability_and_visualization |
| Method | ACE (Attribution-Controlled Knowledge Editing) |
| Dataset | MQuAKE-3K, MQuAKE-3K (Efficacy/Paraphrase/Specificity) |

> [!tip] 效果简介
> - MQuAKE-3K 上，多跳准确率 (Average Accuracy %) 为 ACE: 46.45 (GPT-J), 58.24 (Qwen3-8B)，对比 PMET: 37.01 (GPT-J), 20.78 (Qwen3-8B)，变化 +9.44% (GPT-J), +37.46% (Qwen3-8B)。
> - MQuAKE-3K (Efficacy/Paraphrase/Specificity) 上，Efficacy, Paraphrase, Specificity (%) 为 ACE-Efficacy: 99.8/99.4 (GPT-J/Qwen3-8B), Paraphrase: 91.2/94.2，对比 PMET-Efficacy: 94.2/93.1, Paraphrase: 87.6/88.5 (GPT-J/Qwen3-8B)，变化 Efficacy: +5.6/+6.3, Paraphrase: +3.6/+5.7。

## 概要

大型语言模型（LLM）在知识编辑任务中面临一个关键瓶颈：现有方法在编辑单跳事实时表现良好，但在需要多跳推理的场景中性能急剧下降。其深层原因在于，多跳推理中隐式主语作为"查询神经元"依次激活各层"值神经元"以累积信息的"查询-值"神经通路被广泛忽视——传统方法仅编辑存储事实的值神经元，却没有调整触发这些值神经元的查询机制，导致推理链断裂，更新后的知识无法被正确激活和传递。

本文提出 **ACE（Attribution-Controlled Knowledge Editing）**，一种基于归因控制的知识编辑框架。ACE的核心创新在于从"仅编辑值神经元"的层面，升级为"同时编辑深层值神经元与中层查询神经元"的协同干预。它首先利用神经元级的归因指标——值神经元重要性分数 $\mathcal{I}(v^l)$（公式9）和查询神经元激活潜力 $\mathcal{T}_{query}$（公式10）——识别出对多跳推理至关重要的查询层和值层；随后在值层通过闭式解（公式12）精确更新存储的事实内容，在查询层通过优化KL散度与负对数似然的组合目标（公式13）微调查询参数，确保新知识在下游推理链中能被正确激活。

实验结果表明，ACE在MQuAKE-3K基准上相比最强基线PMET，**在GPT-J上多跳准确率提升9.44%（46.45% vs 37.01%），在Qwen3-8B上提升37.46%（58.24% vs 20.78%）**。消融实验进一步揭示了因果机制：移除值层编辑导致准确率骤降40.45%，而移除查询层编辑导致下降16.51%，验证了值层对知识存储的核心作用以及查询层对推理激活的不可或缺性。此外，ACE在反事实编辑场景和通用基准上均保持了良好的局部性，未造成灾难性遗忘。



大语言模型在注入新事实时大多依赖"定位-编辑"（locate-then-edit）式知识编辑方法，如ROME、MEMIT等，通过因果追踪识别并修改深层FFN中的少数神经层。这些方法在单跳事实更新上表现优异，但在多跳事实回忆（multi-hop factual recall）场景中准确率急剧下降，其根本瓶颈在于：**编辑中间隐式主语时，模型内部隐式主语作为"查询神经元"动态激活"值神经元"的过程被完全忽视，导致推理链无法正确传递更新后的知识**。如图1所示，当多跳推理路径中某个中间事实被修改后，模型必须沿着新的链（如"篮球→足球→国家"）进行推理，但现有方法仅更新了存储信息的值神经元，并未调整激活这些存储单元的查询机制，造成隐式主语新引入的信息无法被后续层有效提取。

因果干预实验提供了直接证据：对语义相关的前1%关键神经元施加干预即可导致准确率下降超过90%，而随机干预的降幅不足10%，这证实了少数关键神经元主导着事实信息的累积与传递。进一步的分析揭示，在多跳推理中，**大型语言模型通过依次执行"查询-值"相互作用来累积信息：查询神经元（由隐式主语触发）顺序激活各层的值神经元，逐步将证据汇聚到最终答案**。表1显示，GPT-J中的关键注意力层（a27, a26, a7等）和FFN层（f27, f26, f7等）确实按任务-语义类型呈现稳定的重要性排序，表明查询-值通路具有可定位的结构化模式。现有方法仅编辑值神经元（深层FFN），而未触及中层查询神经元，因此在多跳编辑中遭遇性能崩塌。

这一因果认知促使ACE的提出：**知识编辑不仅要更新存储事实的值神经元，还需调整激活这些值神经元的查询神经元，以保障多跳推理链的通畅**。该方法跳出了传统的层粒度启发式，在神经元粒度上通过归因重要性分数定位关键的查询层与值层，并分别完成互补编辑。消融实验则强化了动机——移除查询层编辑导致GPT-J平均多跳准确率下降16.51%，而移除值层编辑则骤降40.45%，表明值层对知识存储更关键，而查询层对激活路径必不可少。在同等编辑层数下，仅增加值编辑层数对基线提升有限，进一步暴露了仅编辑值神经元的知识瓶颈，从而凸显同时优化查询-值交互的必要性。



## 核心方法与创新机理

ACE 的核心创新在于**首次将多跳事实编辑的瓶颈从"存储知识的值神经元"扩展到"激活该知识的查询神经元"**，并构建了基于归因的控制框架来精确识别与同时编辑这两类关键通路的神经元。

现有定位-编辑范式（如 ROME、MEMIT、PMET）默认仅修改深层 FFN 中的值神经元，忽视了一个关键机制：在多跳推理中，**隐式主语充当查询神经元，顺序激活各层值神经元以累积信息**。仅更新值神经元无法保证更新后的知识在下游被正确激活，导致推理链断裂——这是已有方法在多跳场景中性能骤降的根本原因（MQuAKE-3K 上最强基线 PMET 在 GPT-J 仅 37.01%，Qwen3-8B 仅 20.78%）。

ACE 通过以下**三个 Changed Slot** 系统性地解决了上述问题：

1. **编辑对象**：从"仅值神经元（深层 FFN）"变为"关键查询神经元与值神经元（深层值 + 中层查询）"。  
   - **依据**：消融实验表明，略过查询层导致准确率下降 **16.51%**，而略过值层导致更严重的 **40.45%** 下降，证实两者均为必要组件（Table 4）。编辑对象扩展后，同等编辑层数下 ACE 大幅超越仅编辑值神经元的基线（例如 GPT-J 上 #9-ACE 46.45 vs #9-PMET 38.29；Table 6），暴露了纯值神经元的"知识瓶颈"。

2. **层/神经元选择依据**：从"基于因果追踪的层启发式选择"变为"基于归因的重要性分数（$\mathcal{I}$ 和 $\mathcal{T}_{query}$），在**神经元粒度**上选择关键组件"。  
   - **依据**：通过值神经元重要性分数 $\mathcal{I}(v^l) = \log p(w \mid v^l + h^{l-1}) - \log p(w \mid h^{l-1})$（公式 9）和查询神经元激活潜力 $\mathcal{T}_{query} = \boldsymbol{v} \cdot fc1_k^l$（公式 10），ACE 能够精确定位对目标令牌贡献最大的值神经元和激活值神经元最多的查询层，而无需依赖单一启发式层。因果干预实验（Figure 2）显示，对 Top 1% 的语义相关神经元进行干预即可导致准确率下降 **>90%**，而随机干预下降不足 10%，验证了稀疏关键神经元的存在，也表明粗粒度的层选择会浪费编辑容量。

3. **多跳推理处理**：从"忽视隐式主语在推理链中的动态激活过程"变为"显式建模查询-值交互，在编辑时**同时更新激活路径（查询）和存储内容（值）**"。  
   - **依据**：ACE 在识别阶段利用归因分数定位中层查询层和深层值层（Figure 4 示意），编辑阶段先通过闭式解更新值神经元权重（公式 11-12），再通过微调查询神经元参数（优化目标含 KL 散度与负对数似然，公式 13）以确保更新后的信息能被正确激活和传递。这套机制使得 ACE 在多跳准确率上较最强基线 PMET 分别提升 **+9.44%**（GPT-J）和 **+37.46%**（Qwen3-8B）（Table 2），同时在 Efficacy 与 Paraphrase 上也全面优于现有方法（Table 3），且未损害局部性（Table 19）及反事实编辑下的鲁棒性（Table 18）。

综上，ACE 的核心创新并非简单的编辑目标扩增，而是**打通了从机制理解到干预体系的闭环**：在定位上采用可加和归因分数的稀疏神经元选择，在编辑上区分值（知识存储）和查询（知识激活）的角色，并通过两阶段优化实现高效协同更新，从根本上解决了多跳推理链断裂的问题。



![[assets/figures/papers/iclr26_0005_IuWIzmMvKo_ACE_Attribution-Controlled_Knowledge_Editing_for/figures/005_Figure_4.jpg]]
*Figure 4: ACE edits Q-V neurons via attribution: (a) The existing locate-then-edit KE method updates new fact using a single-hop prompt; (b) For multi-hop factual recall tasks, traditional locate-then-edit failed to correct edit the knowledge on query layers, overlooking value neurons; (c) Our ACE identifies critical query layers which activates the value neurons most to edit the knowledge*

ACE 方法的提出源于一个关键瓶颈：现有知识编辑方法在多跳事实回忆中性能严重下降，其根本原因在于它们仅更新深层 FFN 中的**值神经元（value neurons）**，却忽视了**隐式主语作为查询神经元（query neurons）逐层激活值神经元**这一动态过程，导致更新后的知识无法在推理链中被正确触发和传递。

为打通这一 **查询-值（Q-V）通路**，ACE 采用 "归因识别 → 值编辑 → 查询编辑" 的两阶段流水线：

### 输入
- 一组新的知识三元组（如 `(Mark Trumbo, plays, Football)`、`(Football, located in, Italy)`）及相应的多跳提示；
- 预训练语言模型（如 GPT-J、Qwen3-8B）；
- 少量上下文示例（in-context priming）。

### 阶段一：关键通路识别
针对每一条待编辑事实，前向计算模型在正确答案 token 上的两项归因指标：
- **值神经元重要性** $\mathcal I(v^l)$（公式 9）：通过注入单个神经元的输出向量并观测对数概率的增量，衡量该神经元对目标 token 的贡献；归一化后得到层的总分 $\mathcal I(l)$。
- **查询神经元激活能力** $\mathcal T_{query}$（公式 10）：计算残差向量与 FFN 子键（`fc1` 权重）的内积，反映查询神经元激活对应值神经元的潜力，同样可聚合到层级别 $\mathcal T_{query}(l)$。

根据分数高低，自动选出 top-$k$ 个**查询层**（多位于中层）和**值层**（多位于深层），作为后续编辑的目标组件（Figure 4、Table 1）。

### 阶段二：双重编辑
在识别出的层上依次执行两类互补的参数更新：

1. **值神经元编辑（Value Edit）**  
   在选中的深层 FFN 上，通过求解带正则的线性最小二乘问题（公式 11），在保留原有知识协方差先验 $C_0$ 的前提下植入新事实，得到闭式增量权重：
   
$$
\Delta = R K_E^\top (C_0 + K_E K_E^\top)^{-1}, \quad R = V_E - W_{fc2}^l K_E
$$

   （公式 12）。这一步将新知识直接写入值神经元的输出空间。

2. **查询神经元编辑（Query Edit）**  
   随后在选中的中层 FFN 上，通过最小化同时包含 KL 散度项（保持原行为）和负对数似然项（强制输出正确目标）的损失函数（公式 13），微调查询神经元的参数（`fc1` 权重），确保下游隐式主语能有效激活刚刚更新的值神经元，使正确信息沿推理链传递。

### 输出
仅更新选定的查询层与值层 FFN 子模块后的模型。该模型在保持原有一般知识（Table 19）的同时，显著提升多跳事实回忆的准确率——相较最强基线 PMET，**GPT-J 上提高 9.44%，Qwen3-8B 上提高 37.46%**（Table 2）。

### 设计原理与证据
ACE 框架的核心创新在于将传统"仅编辑值神经元"的单点干预，扩展为**同时修复值存储与查询激活路径**。消融实验有力地支撑了这一设计：在 GPT-J 上，移除查询层编辑导致多跳准确率下降 **16.51%**，而仅移除值层编辑更是导致 **40.45%** 的剧烈下降（Table 4），说明值层对知识存储更为关键，查询层对推理链的导通必不可少。此外，即使使用相同的编辑层数，ACE 也远超仅编辑值神经元的 ROME、MEMIT 和 PMET（Table 6），进一步揭示那些方法存在**知识瓶颈**，即单纯增加值编辑层数无法弥补查询通路被忽略所带来的损害。

ACE 的归因分数可在编辑前预计算并缓存，使得单次更新仅需约 3 秒（GPT-J），具备实用效率（附录 J）。该框架的主要局限在于，归因分数的计算依赖当前数据分布，在全新模型或未见过的关系类型上可能需重新执行阶段一，增加部署成本；其适用性目前主要验证于解码器型 Transformer，在其他架构上的有效性仍有待确认。



ACE 的核心思路是将知识编辑从以往的层启发式"定位—编辑"范式推进到神经元粒度的归因控制，通过解耦并联合更新**查询神经元**与**值神经元**来修复多跳推理中被破坏的"查询-值"通路。方法可以分解为三个关键模块，每个模块都有明确的优化目标和可操作的计算形式。

### 关键通路识别
多跳推理中，隐式主语作为查询神经元依次激活各层的值神经元以累积证据；但现有方法通常只更新存有事实的深层值神经元，导致上游查询神经元仍保留旧激活模式，推理链断裂。ACE 首先在神经元粒度上量化每个候选组件对目标令牌的贡献，据此确定需要编辑的**关键查询层**与**值层**。

对于任意第 $l$ 层的值神经元 $v^l$，其重要性通过向隐藏状态中注入该神经元向量后的对数概率增益来度量（式 9）：

$$
\mathcal{I}(v^l) = \log p(w \mid v^l + h^{l-1}) - \log p(w \mid h^{l-1}),
$$

其中 $h^{l-1}$ 是前一层输出的隐藏状态，$w$ 为目标令牌。层重要性则定义为层内所有神经元重要性之和 $\mathcal{I}(l) = \sum_{v \in l} \mathcal{I}(v^l)$。这一方法基于因果干预的思想，直接测量单神经元对最终预测的边际贡献，而非间接定位注意力或 FFN 单层。

查询神经元的激活能力由当前残差向量与 FFN 子键（fc1 权重）的内积刻画（式 10）：

$$
\mathcal{T}_{query}(v^l) = v \cdot fc1_k^l,\quad \mathcal{T}_{query}(l) = \sum_{v \in l} \mathcal{T}(v^l),
$$

其中 $v$ 为当前残差流中的向量（即进入 FFN 的输入），$fc1_k^l$ 为第 $l$ 层第 $k$ 个神经元的子键向量。该分数越高，表示对该值神经元的激活潜力越大。按照以上两个指标排序，即可分别在深层选出值层、在中层选出查询层作为编辑对象，将注意力聚焦于最易阻断多跳推理的瓶颈神经元群。

### 值神经元编辑
在识别出的深层值层上，ACE 修改 FFN 的第二层权重 $\hat{W}$，使得新知识被植入的同时尽可能保留模型原有行为。优化的权衡目标为（式 11）：

$$
\operatorname{argmin}_{\hat{W}} \left( \lambda \| \hat{W} K_0 - W_{fc2}^l K_0 \|^2 + \| \hat{W} K_E - V_E \|^2 \right),
$$

这里 $K_0$ 是用于保留原有知识的键（key）表示集合，$K_E$ 和 $V_E$ 分别对应待编辑知识的键和期望输出的值表示；$W_{fc2}^l$ 是当前 FFN 第二层的原始权重，$\lambda$ 控制保留强度。该优化可得到闭式增量解（式 12）：

$$
\Delta = R K_E^{\top} (C_0 + K_E K_E^{\top})^{-1},\quad
R = V_E - W_{fc2}^l K_E,\quad
C_0 = K_0 K_0^{\top}.
$$

权重被更新为 $\hat{W} = W_{fc2}^l + \Delta$。由于通过 $C_0$ 维持了原有知识的协方差先验，此步骤能够以较低的成本对值层进行精确编辑，避免灾难性遗忘。

### 查询神经元编辑
仅修改值层无法保证更新后的信息在推理中能被正确激活，因此 ACE 进一步对已识别出的中间查询层做轻量扰动，通过微调查询神经元的输出向量来调整激活路径。优化目标同时考虑行为保持和编辑精度（式 13）：

$$
\delta = \operatorname{argmin}_{\delta} \mathcal{L}(\delta) = \mu D_{\mathrm{KL}}(P_{\mathcal{M}_e}[t' \mid T] \| P_{\mathcal{M}}[t' \mid T]) + \varphi \frac{1}{P} \sum_{j=1}^{P} -\log \mathbb{P}_{\mathcal{M}_e}[o^* \mid \mathrm{pref}_j \oplus T_e],
$$

其中 $\delta$ 是施加在查询向量上的扰动；第一项通过 KL 散度约束编辑后模型 $\mathcal{M}_e$ 在原始上下文 $T$ 上的预测分布，防止无关行为漂移；第二项在 $P$ 条编辑提示下最大化目标令牌 $o^*$ 的对数似然，确保新关联被激活。超参数 $\mu$ 和 $\varphi$ 分别控制保留与编辑的强度。查询层编辑只引入少量参数扰动，却显著恢复了多跳推理中由隐式主语触发的级联激活路径，使得值层写入的新证据能够被正确传导。

三个模块共同实现了对查询-值通路的完整编辑：关键通路识别提供了归因驱动的神经元选择依据，值编辑负责知识存储的更新，查询编辑则保障了更新后的信息在推理链中的传递效率。



## 实验与关键发现

### 主实验结果

在多跳事实编辑基准 MQuAKE-3K 上，ACE 在 GPT-J 与 Qwen3-8B 分别取得平均多跳准确率 46.45% 和 58.24%，相比当前最强基线 PMET（37.01% / 20.78%）提升了 **+9.44** 与 **+37.46** 个百分点（Table 2）。ACE 的编辑质量同样领先：GPT-J 上 Efficacy 达 99.8%（PMET 为 94.2%），Paraphrase 达 91.2%（PMET 为 87.6%），表明编辑结果精确且表述鲁棒性更强（Table 3）。随着同时编辑的事实条数增加，ACE 的优势愈发明显——修改 4 条事实时 ACE 仍保持 25.12% 的准确率，而其他方法普遍跌破 16%，显示出查询-值通路协同编辑对长推理链的支持。

![[assets/figures/papers/iclr26_0005_IuWIzmMvKo_ACE_Attribution-Controlled_Knowledge_Editing_for/figures/006_Table_2.jpg]]
*Table 2: Multi-hop accuracy comparison of different KE methods on the MQuAKE-3K dataset in a few-shot setting, Base shows the model's performance on the unedited answers and edited model's performance on edited answers. Our model outperformances than other models significantly*

### 消融实验

**查询层与值层的不可替代性**  
移除查询层编辑（跳过重要性最高的查询层）在 GPT-J 上导致平均准确率下降 **16.51%**，而移除值层编辑造成降幅达 **40.45%**（Table 4）。值层的更大损失阐明其是事实存储的核心，但查询层缺失仍严重削弱性能，证明激活更新推理路径必须同时修改查询表征。

![[assets/figures/papers/iclr26_0005_IuWIzmMvKo_ACE_Attribution-Controlled_Knowledge_Editing_for/figures/008_Table_4.jpg]]
*Table 4: The results of ablation experiments on GPT-J-6B and Qwen3-8B model. The column Editor shows which layer(s) are skipped in the editing process, the index # of the layer refers to the importance rank. The percentage of decrease(↓) is calculated relative to ACE as the baseline*

**编辑层数与知识瓶颈**  
在相同编辑层数下（如 GPT-J 上均编辑 9 层），ACE（46.45%）大幅超越仅编辑值神经元的 ROME（37.98%）、MEMIT（39.47%）和 PMET（38.29%）（Table 6）。单纯增加值编辑层数对基线方法提升十分有限（MEMIT 从 7 层到 9 层仅从 38.98% 升至 39.47%），这暴露了纯值编辑存在**知识瓶颈**：即便植入更多正确事实，旧的查询通路仍会错误激活过时的值，限制多跳推理表现。

![[assets/figures/papers/iclr26_0005_IuWIzmMvKo_ACE_Attribution-Controlled_Knowledge_Editing_for/figures/010_Table_6.jpg]]
*Table 6: Analysis of number of edited layers on GPT-J and Qwen3-8B*

**上下文鲁棒性初步观察**  
在不同 Chain-of-Thought 提示下的消融（Table 5）显示 ACE 对上下文变化的敏感度较低，稳定性较好。**该结论的置信度中等（≈0.8），需进一步实验确认。**

### 关键图表与因果证据

**Figure 2** 的因果干预强有力地验证了关键神经元的因果角色：对重要性前 1% 的语义相关神经元进行干预，导致准确率下降超过 90%；而随机选择神经元的干预仅引起不足 10% 的下降，直接支持了归因分数的可靠性。  
**Table 1** 给出了 GPT-J 中重要性排名前 9 的注意力层与 FFN 层，深层注意力层（如 a27）和 FFN 层（如 f27）的频繁出现，与深层存值、中层至深层注意力负责查询激活的分工一致。  
**Table 7** 从 token 粒度揭示了残差流上重要性的激增模式：关键字"plays"使 FFN 重要性分数飙升至 0.9846，注意力重要性达 0.8167，并在词汇空间激活相关属性词，细化了查询-值交互的时序过程。

![[assets/figures/papers/iclr26_0005_IuWIzmMvKo_ACE_Attribution-Controlled_Knowledge_Editing_for/figures/003_Figure_2.jpg]]
*Figure 2: The Impact of Causal Intervention with semantic-related requests upon LLMs of most important layer, including Nationality, Continent, Capital and Language requests*

![[assets/figures/papers/iclr26_0005_IuWIzmMvKo_ACE_Attribution-Controlled_Knowledge_Editing_for/figures/002_Table_1.jpg]]
*Table 1: Top 9 important attention layers (left block) and FFN layers (right block) in GPT-J*

### 局限性与开放问题

- 归因计算依赖预计算分数，对新模型或分布需重新计算，部署成本较高。
- 当前验证仅基于解码器 Transformer（GPT-J、Qwen3-8B），对其他架构的适用性未知。
- 任务限于多条事实编辑，连续多次编辑或需要修改推理规则的场景的扩展性有待探索。
- 查询层与值层的划分仍部分依赖语义类型的先验，自动化程度可进一步提升。

未来的关键开放问题包括：值编辑器的知识瓶颈是否源于模型容量或残差流表示约束；稀疏关键神经元的普遍性及动态确定数量的方法；多轮编辑后表征漂移与编辑冲突的鲁棒防遗忘机制；以及如何利用训练后强化学习塑造的语义激活模式进一步增强编辑性能。

（以上结论均基于 MQuAKE-3K 少样本设置，指标覆盖 Efficacy、Paraphrase、Specificity 及通用基准上的局部性，保证了评估的全面性。）



## 定位与知识库关联

### 从单点编辑到通路编辑的范式跃迁

ACE (Attribution-Controlled Knowledge Editing) 的提出源于一个关键瓶颈：现有知识编辑方法在多跳事实回忆中性能严重下降。定位-编辑范式的基线方法 (ROME、MEMIT、PMET、IFMET) 共享一个隐式假设——编辑深层 FFN 中的"值神经元"即可完成知识更新。然而，在多跳推理场景中，模型通过"查询-值"交互逐步累积信息：中间隐式主语作为查询神经元，依次激活下游层的值神经元，形成完整的推理链。当编辑仅修改值神经元时，激活这些神经元的查询通路未被调整，导致更新后的知识无法沿推理链正确传递。ACE 的核心创新在于将编辑对象从"值神经元"扩展为"查询-值神经通路"，实现了从单点编辑到通路编辑的范式跃迁。

### 方法谱系中的差异定位

ACE 与主要基线方法的核心差异体现在三个维度：

| 维度 | 基线方法 | ACE |
|------|----------|-----|
| **编辑对象** | 仅值神经元（深层 FFN） | 查询神经元 + 值神经元（深层值 + 中层查询） |
| **层选择依据** | 基于因果追踪的层启发式搜索 | 基于归因的重要性分数（I 和 T_query），在神经元粒度选择 |
| **多跳推理处理** | 忽视隐式主语的动态激活过程 | 显式建模查询-值交互，同时更新激活路径和存储内容 |

ROME 奠定了定位-编辑范式，通过因果追踪定位关键 FFN 层并施加秩一更新；MEMIT 将其推广至多层同时编辑；PMET 进一步区分 MHSA 和 FFN 的角色，采用层次化编辑；IFMET 针对多跳场景构造特殊提示以编辑更深层 FFN。然而，消融实验揭示了一个关键证据：在相同编辑层数下（如 GPT-J 上的 #9 配置），ACE 的多跳准确率（46.45%）显著优于仅编辑值神经元的基线（ROME 37.98%、MEMIT 39.47%、PMET 38.29%），且为基线增加更多值编辑层仅带来边际提升，暴露了仅编辑值神经元的固有知识瓶颈。

### 查询-值通路的因果证据

ACE 通路编辑的必要性由多条因果证据支撑。Figure 2 显示，对前 1% 语义相关神经元的因果干预导致准确率下降超过 90%，而随机干预下降不足 10%，验证了稀疏关键神经元的存在。消融实验进一步量化了各通路的贡献：移除查询层编辑导致 GPT-J 平均准确率下降 16.51%，而移值层编辑导致骤降 40.45%，表明值层对知识存储更为关键，查询层则是激活路径的必要组件。这一结果解释了为何仅编辑值层的基线方法在多跳场景失效：它们更新了存储内容，却未修复触发提取的激活通路。

ACE 方法的两个阶段对应上述发现：Stage 1 使用归因指标（重要性分数 I 和 T_query）在神经元粒度识别关键查询层和值层；Stage 2 分别对深层值层施加闭式解权重更新（公式 11-12），对中层查询层进行参数微调（公式 13），以确保更新后的知识能被下游正确激活。pipeline 的可解耦性（识别与编辑）也为 ACE 向后续知识编辑方法扩展提供了便利。

### 适用边界与条件限制

ACE 的性能增益依赖于模型内部"查询-值"交互通路的存在，当前主要在解码器型 Transformer（GPT-J、Qwen3-8B）上验证，对编码器-解码器架构的适用性未知。方法使用预计算的归因分数确定关键层，在全新模型或未见过的数据分布下需要重新计算，增加了部署成本。此外，查询层和值层的划分基于对语义类型的先验分类（如国籍、首都等），自动化程度有限，在更广泛的编辑场景中可能需要人为调整。

实验覆盖了反事实编辑场景，ACE 在 Efficacy（89.7%/91.2%）和 Paraphrase（83.6%/80.7%）指标上均保持合理水平，且在通用基准（CSQA、BBH、MMLU、GSM8k）上未造成灾难性遗忘。然而，所有实验均在 MQuAKE-3K 的少样本设置下进行，方法在更复杂的多任务编辑、长序列编辑或连续多次编辑后的表征漂移问题尚待检验。

### 开放问题与未来方向

1. **知识瓶颈的机制解析**：消融实验中仅增加值编辑层对基线方法提升有限，这一瓶颈是否源于 FFN 的容量限制或残差流的表示约束？理解其机制可能为编辑方法设计提供新思路。
2. **稀疏神经元的普适性**：当前发现的稀疏关键神经元（如 27 个关键神经元）是否在其他规模的模型架构中普遍存在？能否动态而非经验性地确定最优神经元数量？
3. **从事实到推理的编辑推广**：ACE 的归因框架能否扩展到修改推理规则（而非事实知识）的场景？这可能需要重新定义"查询"和"值"的语义。
4. **连续编辑的鲁棒性**：连续多次编辑后的模型内部表征漂移是否会导致编辑冲突？如何设计更鲁棒的防遗忘机制以支持增量式知识更新？
5. **后训练强化学习的影响**：Post-training RL 如何塑造语义激活模式？能否将其作为先验信息进一步提升编辑效能？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/ACE_Attribution_Controlled_Knowledge_Editing_for_Multi_hop_Factual_Recall.pdf

![[paperPDFs/ICLR_2026/ACE_Attribution_Controlled_Knowledge_Editing_for_Multi_hop_Factual_Recall.pdf]]
