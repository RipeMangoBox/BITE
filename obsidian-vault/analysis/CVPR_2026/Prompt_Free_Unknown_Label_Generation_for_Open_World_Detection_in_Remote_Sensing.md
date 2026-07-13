---
title: Prompt-Free Unknown Label Generation for Open World Detection in Remote Sensing
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Prompt_Free_Unknown_Label_Generation_for_Open_World_Detection_in_Remote_Sensing.pdf
project_link: null
code_link: null
aliases:
- PFULGOWDRS
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 基于层级语义图的场景条件化分类（Deformable Hierarchical Graph Attention, DHGA）与上下文感知的区域到文本嵌入合成（Context-Aware Region-to-Text, CR2T）。
primary_logic: 利用空间共现模式驱动层次化语义图上的粗到细分类，并通过融合视觉特征、场景上下文令牌和层级父节点信息，在不依赖外部语言模型的情况下为未知对象生成可用的语义标签，实现检测与自主命名的统一。
claims:
- HSGDet在已知mAP上较现有最佳方法提升6.6点，在未知召回上提升9.9点，并将Wilderness Impact降低36%。
- CR2T模块合成的语义嵌入与真实CLIP嵌入的余弦相似度达到0.79，无需外部语言模型。
- 完整的HSGDet通过DHGA和CR2T的组合，在DOTA-v2上取得54.8 K-mAP, 41.2 U-R和5.8 WI，显著超越OW-OVD等基线。
- DOTA-v2 上 Known mAP (K-mAP) = 54.8
---

# Prompt-Free Unknown Label Generation for Open World Detection in Remote Sensing

> [!tip] 核心洞察
> 利用空间共现模式驱动层次化语义图上的粗到细分类，并通过融合视觉特征、场景上下文令牌和层级父节点信息，在不依赖外部语言模型的情况下为未知对象生成可用的语义标签，实现检测与自主命名的统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | 遥感开放世界检测中无提示的未知标签生成 |
| 英文题名 | Prompt-Free Unknown Label Generation for Open World Detection in Remote Sensing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Azeem_Prompt-Free_Unknown_Label_Generation_for_Open_World_Detection_in_Remote_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | HSGDet |
| Dataset | DOTA-v2, FAIR1M, DIOR, COCO |

> [!tip] 效果简介
> - DOTA-v2 上，Known mAP (K-mAP) 54.8 vs OW-OVD: 48.2 (+6.6)；Unknown Recall (U-R) 41.2 vs OW-OVD: 31.3 (+9.9)；Wilderness Impact (WI) 5.8 vs OW-OVD: 9.1 (-36%)。
> - FAIR1M 上，K-mAP / U-R / WI 52.4 / 38.5 / 6.2。
> - DIOR 上，K-mAP / U-R / WI 59.3 / 42.8 / 5.2。

## 概要

遥感图像中的开放世界目标检测面临一个长期瓶颈：现有方法能够发现训练时未见过的未知对象，却无法为其赋予语义标签——它们要么将未知对象简单标记为匿名的“unknown”，要么依赖外部语言提示或人工标注。这种语义缺失严重制约了遥感监测任务的全自主部署能力。

HSGDet 针对这一瓶颈提出了“无提示未知标签生成”范式。其核心机制由两个因果调节器构成：**可变形层次图注意力（Deformable Hierarchical Graph Attention, DHGA）** 和 **上下文感知的区域到文本嵌入合成（Context-Aware Region-to-Text, CR2T）**。DHGA 利用场景上下文令牌（Scene Context Token, SCT）捕获的空间共现模式，在基于 WordNet 构建的层次语义图上执行场景条件化的粗到细分类，将目标查询路由至已知类别或标记为未知。CR2T 则接收被标记为未知的查询，融合其视觉特征、场景上下文以及层次父节点的语义嵌入，在不依赖外部语言模型的情况下直接合成未知对象的 CLIP 文本嵌入，并通过缓冲-聚类机制将新类别节点动态注册到语义图中，实现持续词汇扩展。

实验结果表明，HSGDet 在 DOTA-v2 上取得了 54.8 K-mAP 和 41.2 U-R，较现有最佳方法 OW-OVD 分别提升 6.6 点和 9.9 点，同时将 Wilderness Impact 降低 36%。CR2T 合成的语义嵌入与真实 CLIP 文本嵌入的余弦相似度达到 0.79。在 FAIR1M、DIOR 和 COCO 等数据集上的跨域评估进一步验证了方法的泛化能力。定性对比显示，HSGDet 能够为未知对象赋予具体类别标签（如“lamp”），而 OWOBJ 仅能将其标记为“unknown”。

在方法谱系上，HSGDet 位于开放世界检测与开放词汇检测的交汇地带，其基线参照包括 **OW-DETR**（Gupta et al., CVPR 2022）、**CAT**（Ma et al., CVPR 2023）、**PROB**（Zohar et al., CVPR 2023）、**UC-OWOD**（Wu et al., ECCV 2022）、**OW-OVD**（Xi et al., CVPR 2025）和 **SkySense-O**（Zhu et al., CVPR 2025）等。与这些方法不同，HSGDet 将层次语义图作为可扩展的知识库，通过场景条件化导航和嵌入合成，首次实现了检测与自主命名的统一。



### 开放世界目标检测的范式演进

目标检测在深度学习推动下取得了显著进展，但传统闭集检测器只能识别训练阶段预定义的固定类别集合。在遥感监测、自动驾驶等真实场景中，模型不可避免地会遭遇训练时未曾见过的对象类别，这催生了两种重要的检测范式：

- **开放词汇检测（Open-Vocabulary Detection, OVD）**：利用视觉-语言模型（如CLIP）的泛化能力，通过文本提示检测任意类别。然而，OVD本质上需要用户提供目标类别的文本提示，无法自主发现提示之外的新对象。
- **开放世界检测（Open-World Detection, OWOD）**：旨在同时检测已知类别并识别未知对象。现有OWOD方法能够将未知对象标记为“unknown”，但**无法赋予任何语义标签**——它们只知道“这里有个东西”，却不知道“这个东西是什么”。

图1清晰地展示了上述范式的差异：在包含“car”、“house”和“lamp”的遥感场景中，OVD仅检测提示中指定的类别；OWOD虽能发现“lamp”为未知对象，却只能以匿名“unknown”标记；而近期统一OW-OVD框架虽尝试融合两者，仍未解决未知对象的语义命名问题。

### 遥感领域的独特挑战

遥感图像具有俯瞰视角、目标尺度变化大、空间共现模式丰富等特点。例如，飞机通常出现在机场跑道附近，船舶与港口码头高度共现。这些空间共现模式蕴含着重要的语义线索，但现有开放世界检测方法并未显式建模和利用这种场景层面的上下文信息。

此外，遥感应用（如灾后评估、军事侦察）往往需要在无人工干预的条件下全自主运行——系统不仅需要发现未知对象，还必须为这些对象生成可理解的语义标签，以便下游决策系统使用。依赖外部语言模型或手工标注的方案无法满足这种部署需求。

### 现有方法的核心瓶颈

综合分析，当前开放世界目标检测方法存在三个递进式的瓶颈：

1. **语义标签缺失**：发现的未知对象仅被标记为匿名“unknown”，无法为下游任务提供可操作的语义信息。
2. **外部依赖过重**：少数尝试为未知对象命名的方案依赖外部语言模型或用户提示，破坏了系统的自主性。
3. **场景上下文未利用**：遥感图像中丰富的空间共现模式未被有效建模，限制了未知对象推理的准确性。

### 本文的核心动机

针对上述瓶颈，本文提出HSGDet，核心动机是实现**无提示的未知对象自主发现与语义标签生成**。具体而言：

- **自主命名**：在不依赖任何外部语言模型或人工提示的条件下，为检测到的未知对象合成语义嵌入并赋予类别标签。
- **场景条件化推理**：通过显式建模场景上下文和空间共现模式，驱动层次化语义图上的粗到细分类，提升已知与未知对象的判别能力。
- **持续词汇扩展**：设计缓冲-聚类机制，使语义图能够动态注册新类别节点，实现检测能力的持续增长。

这一设计使得HSGDet在遥感开放世界检测任务中，首次实现了从“发现未知”到“理解未知”的跨越。



## 核心方法与创新机理

HSGDet的核心创新在于将开放世界目标检测从“被动标记未知”推向“自主发现并命名未知”，其关键突破体现在三个相互耦合的changed slots上。

### 从线性分类到场景条件化层次语义导航

传统开放世界检测器（如**OW-DETR**、**CAT**、**PROB**）依赖标准线性分类头或基于提示文本的匹配来完成已知类别的识别，而HSGDet引入了**Deformable Hierarchical Graph Attention (DHGA)**，将分类过程重构为在层次语义图上的场景条件化粗到细导航。该机制的核心因果链条如下：

1. **场景上下文感知**：引入可学习的场景上下文令牌（Scene Context Token, SCT）$c$，通过交叉注意力聚合所有目标查询的共现信息：
   $$c_{\mathrm{new}} = \mathrm{CrossAttn}(c_{\mathrm{prev}}, q_i, q_i)$$
   随后以残差方式注入每个查询：
   $$\tilde{q}_i = q_i + c_{\mathrm{new}}$$
   这使模型能够利用“飞机与跑道共现”等遥感场景中的典型空间模式来约束语义推理。

2. **自适应层次路径选择**：基于查询与语义图中各节点可学习键的相似度，通过Top-K采样筛选候选语义节点：
   $$S_i = \mathrm{Top-K}(\mathrm{softmax}(\delta_i), \mathbf{K})$$
   随后计算上下文增强查询与所选节点CLIP文本嵌入的注意力权重：
   $$\beta_{i,v} = \mathrm{softmax}\left(\frac{\tilde{q}_i^T t_v}{\sqrt{d}}\right)$$
   最终通过加权融合更新查询表示：
   $$q_i^{\mathrm{next}} = q_i + \sum_{v \in S_i} \beta_{i,v} t_v$$

3. **已知与未知的分离**：当查询对所有采样节点的最大注意力权重低于阈值$\tau_{\mathrm{unk}}=0.4$时，该查询被判定为“未知”，路由至后续的CR2T模块进行语义标签合成。

消融实验（Table 1）证实了这一设计的有效性：在基线模型上单独添加DHGA使Unknown Recall提升**7.5个百分点**；进一步引入SCT后，U-R再提升**5.8个百分点**，验证了场景共现信息对层次导航的关键支撑作用。

### 从匿名标记到自主语义标签生成

现有方法对检测到的未知对象仅赋予“unknown”这一无信息标签，HSGDet则通过**Context-Aware Region-to-Text (CR2T)**模块实现了无需外部语言模型的自主语义嵌入合成。其核心机制为：

1. **多源信息融合**：对于DHGA标记的未知查询，CR2T首先确定其层次父节点——选择注意力权重最高的采样节点：
   $$v_p = \arg\max_{v \in S_i} \beta_{i,v}$$
   随后通过MLP融合三个互补信息源生成语义嵌入：
   $$t_{\mathrm{new}} = f([q_i^{(\mathrm{final})}; c; t_{v_p}])$$
   其中$q_i^{(\mathrm{final})}$提供视觉外观特征，$c$注入全局场景上下文，$t_{v_p}$提供层次语义先验（如“车辆”作为“卡车”的父节点）。

2. **持续词汇扩展**：生成的嵌入通过缓冲-聚类机制自动注册到语义图中。当缓冲区中$M=5$个嵌入的成对相似度超过阈值$\tau=0.7$时，创建新类别节点：
   $$v_{\mathrm{new}} \gets \{ t_{\mathrm{new}} = \frac{1}{M}\sum_{i=1}^{M} t_i, e_{\mathrm{new}} = e_{v_p}, p(v_{\mathrm{new}}) = v_p \}$$

3. **语义坍塌的防止**：CR2T训练中引入对比损失，迫使生成嵌入靠近真实文本嵌入而远离负样本：
   $$\mathcal{L}_{\mathrm{contrast}}^{i} = \max (0, \cos(t_i^{\mathrm{pred}}, t_i^{\mathrm{neg}}) - \cos(t_i^{\mathrm{pred}}, t_i^{\mathrm{gt}}) + \gamma)$$
   消融实验表明，去除对比损失会导致嵌入坍塌到单一向量，严重损害语义区分能力。

CR2T内部消融（Table 2）揭示了各信息源的关键贡献：完整CR2T（视觉特征+场景上下文+层级父节点）达到文本对齐（TA）**0.79**、语义一致性（SMC）**0.82**和U-R **41.2**，显著优于仅使用视觉特征（TA 0.61, U-R 28.7）或缺少层级父节点（TA 0.72, U-R 34.5）的变体。训练时随机掩盖30%已知类作为伪未知类，可在嵌入质量和未知召回之间取得最佳平衡。

### 创新的协同效应

DHGA与CR2T并非独立运作，而是形成闭环：DHGA利用层次语义图进行场景条件化分类并分离未知查询，CR2T为未知对象合成语义嵌入并回写至语义图，实现词汇的持续扩展。这种协同使HSGDet在DOTA-v2上取得**54.8 K-mAP**、**41.2 U-R**和**5.8 WI**，较统一开放词汇-开放世界检测框架**OW-OVD**（Xi et al., CVPR 2025）分别提升**+6.6点**、**+9.9点**，并将Wilderness Impact降低**36%**。定性对比（Figure 3）进一步显示，**OWOBJ**（Zhang et al., CVPR 2025）仅能将未见对象标记为“unknown”，而HSGDet能赋予其具体类别标签（如“lamp”），实现了检测与自主命名的统一。



HSGDet 的整体设计围绕一个核心目标展开：在遥感开放世界检测中，**无需外部提示或人工标注，即可自主发现未知对象并为其生成语义标签**。为此，模型在标准 Deformable DETR 架构之上，引入了一条“场景感知→层次推理→语义合成→图谱扩展”的闭环流水线。

### 数据流总览

整个推理过程可分为五个阶段，各模块之间的输入输出关系如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2336_https_openaccess_thecvf_com_content_CVPR2026_html_Azeem_Prompt_Free_Unkn/figures/002_Figure_2.jpg]]
*Figure 2: HSGDet architecture. The decoder refines object queries through transformer layers incorporating DHGA and scene context. DHGA performs hierarchical classification while CR2T synthesizes embedding for unknown objects, expanding the semantic graph autonomously*

1. **视觉特征提取**：输入遥感图像首先经过冻结的 CLIP 视觉编码器，提取多尺度视觉特征。该编码器提供冻结的视觉-语言先验，后续所有模块均在此基础上运作，不再调用外部语言模型。

2. **查询初始化与解码**：Deformable DETR 解码器维护一组可学习的对象查询（object queries），通过自注意力、可变形空间交叉注意力逐层精化。在每一解码层中，查询会同时接收来自 DHGA 模块的语义引导和来自场景上下文令牌的全局线索。

3. **场景条件化层次分类（DHGA）**：每个精化后的查询被送入 DHGA 模块。DHGA 在预构建的层次语义图上执行场景条件化的粗到细分类——先利用可学习的场景上下文令牌聚合所有查询的共现模式，再通过 Top-K 节点采样与可学习键匹配，在语义图中沿层次路径导航，最终为每个查询分配类别注意力分布。若某查询对所有已知类别的最大注意力低于阈值 $\tau_{\mathrm{unk}} = 0.4$，则被标记为“未知”，并路由至 CR2T 模块。

4. **上下文感知的区域到文本合成（CR2T）**：CR2T 接收被标记为未知的查询，融合三股信息——最终精化的视觉查询 $q_i^{(\mathrm{final})}$、场景上下文令牌 $c$、以及在语义图中注意力权重最高的父节点文本嵌入 $t_{v_p}$——通过一个三层 MLP（768→512→256，dropout 0.1）合成该未知对象的 CLIP 对齐文本嵌入 $t_{\mathrm{new}}$。

5. **语义图动态扩展**：CR2T 生成的嵌入进入缓冲-聚类机制。当缓冲区中 $M=5$ 个嵌入的成对余弦相似度超过阈值 $\tau = 0.7$ 时，触发新类别节点创建。新节点的文本嵌入取缓冲区均值，可学习视觉键继承自父节点，并以父节点为层次父节点挂载到语义图中，实现持续词汇扩展。

### 关键因果链路

框架中有一条明确的因果链路驱动性能提升：

- **场景上下文令牌（SCT）** 是信息汇聚的枢纽。它通过交叉注意力 $c_{\mathrm{new}} = \mathrm{CrossAttn}(c_{\mathrm{prev}}, q_i, q_i)$ 聚合所有查询的共现信息，再以残差形式 $\tilde{q}_i = q_i + c_{\mathrm{new}}$ 注入每个查询，使分类决策具备场景层面的上下文感知能力。消融实验证实，在 DHGA 基础上引入 SCT 可使 Unknown Recall 额外提升 5.8 个百分点（Table 1）。

- **DHGA 的层次导航** 将分类从扁平匹配转变为路径一致性约束的层次推理。通过层次导航损失 $\mathcal{L}_{\mathrm{hier}}$ 监督目标类在层次路径上的所有祖先节点均获得高注意力，模型学会了沿“粗到细”路径定位类别，这为后续 CR2T 确定未知对象的父节点提供了可靠基础。

- **CR2T 的三源融合** 是生成语义标签质量的关键。仅使用视觉特征（Visual Only）或仅使用视觉+场景上下文（Sibling Context）均无法达到完整 CR2T 的性能——完整 CR2T 在 DOTA-v2 上达到文本对齐 0.79、语义一致性 0.82 和 Unknown Recall 41.2（Table 2）。对比损失 $\mathcal{L}_{\mathrm{contrast}}$ 在此过程中起关键作用，通过最大化正负样本余弦相似度之间的间隔，防止生成嵌入坍塌到单一向量。

### 训练与损失

模型以多任务损失端到端训练：

$$\mathcal{L} = \mathcal{L}_{\mathrm{det}} + \lambda_1 \mathcal{L}_{\mathrm{hier}} + \lambda_2 \mathcal{L}_{\mathrm{CR2T}}$$

其中 $\mathcal{L}_{\mathrm{det}}$ 为检测回归损失，$\mathcal{L}_{\mathrm{hier}}$ 监督层次路径一致性，$\mathcal{L}_{\mathrm{CR2T}}$ 包含对比损失和文本对齐损失（权重 $\lambda_1=0.5$，$\lambda_2=0.3$）。训练时随机掩盖 30% 已知类作为伪未知类，以在 CR2T 嵌入质量和未知召回之间取得最佳平衡。

### 与现有范式的本质差异

Figure 1 清晰展示了 HSGDet 与三种现有范式的区别：OVD 仅检测提示类别，OWOD 将新类别标记为匿名“unknown”，Unified OW-OVD 虽能同时处理已知和未知但未知仍无标签。HSGDet 的独特之处在于，它通过 DHGA 的场景条件化层次推理确定未知对象的语义上下文，再通过 CR2T 在不依赖外部语言模型的情况下合成可用语义标签，从而将“发现未知”与“命名未知”统一在单一框架内，实现了真正的全自主开放世界检测。



HSGDet 的整体架构建立在 Deformable DETR 解码器之上，其核心创新在于两个紧密协作的模块：**可变形层次图注意力（DHGA）** 与 **上下文感知的区域到文本合成（CR2T）**，二者共同驱动一个可动态扩展的 **层次语义图**。以下按模块拆解关键公式与机制。

### 层次语义图构建

层次语义图 $G = (V, E)$ 基于 WordNet 的 IS-A 关系构建，每个节点 $v \in V$ 存储两类嵌入：CLIP 文本嵌入 $t_v$ 和可学习的视觉键嵌入 $e_v$。有向边 $(u,v) \in E$ 表示 $v$ 是 $u$ 的子类别，其邻接矩阵定义为：

$$A_{uv} = \begin{cases} 1, & \text{if } (u,v) \in \mathcal{E} \\ 0, & \text{otherwise} \end{cases} \quad \text{(Eq. 1)}$$

部署阶段，CR2T 合成的新类别节点 $v_{\mathrm{new}}$ 会被添加到其父节点 $v_p$ 之下，实现词汇的动态扩展。

### 场景上下文令牌（SCT）

为将全局场景共现模式注入每个目标查询，HSGDet 引入一个可学习的场景上下文令牌 $c$。在每层解码器中，$c$ 通过交叉注意力聚合所有查询 $q_i$ 的信息：

$$c_{\mathrm{new}} = \mathrm{CrossAttn}(c_{\mathrm{prev}}, q_i, q_i) \quad \text{(Eq. 2)}$$

随后通过残差相加将全局场景线索注入每个查询：

$$\tilde{q}_i = q_i + c_{\mathrm{new}} \quad \text{(Eq. 3)}$$

### DHGA：场景条件化的层次分类

DHGA 在层次语义图上执行粗到细的场景条件化导航，其核心流程如下：

1. **Top-K 节点采样**：基于上下文增强查询 $\tilde{q}_i$ 与各节点可学习键 $e_v$ 的相似度 $\delta_i$，选择得分最高的 $K$ 个语义节点：

$$S_i = \mathrm{Top-K}(\mathrm{softmax}(\delta_i), \mathbf{K}) \quad \text{(Eq. 4--5)}$$

2. **语义融合注意力**：计算查询与所选节点 CLIP 文本嵌入 $t_v$ 的注意力权重：

$$\beta_{i,v} = \mathrm{softmax}\left(\frac{\tilde{q}_i^T t_v}{\sqrt{d}}\right) \quad \text{(Eq. 6)}$$

3. **查询精化**：利用注意力权重加权求和所选节点的文本嵌入，更新查询表示：

$$q_i^{\mathrm{next}} = q_i + \sum_{v \in S_i} \beta_{i,v} t_v \quad \text{(Eq. 7)}$$

4. **已知/未知分离**：当查询的最大注意力权重 $\max \beta_{i,v} < \tau_{\mathrm{unk}} = 0.4$ 时，该查询被标记为未知，路由至 CR2T 模块进行语义标签合成。

### CR2T：未知对象的语义嵌入合成

CR2T 在无需外部语言模型或人工提示的前提下，为被标记的未知查询合成 CLIP 文本嵌入。其关键步骤如下：

1. **父节点选择**：在未知查询的采样节点 $S_i$ 中，选择注意力权重最高的节点作为层次父节点：

$$v_p = \arg\max_{v \in S_i} \beta_{i,v} \quad \text{(Eq. 8)}$$

2. **嵌入合成**：通过一个 3 层 MLP（[768→512→256]，dropout 0.1）融合三个信息源——最终精化后的视觉查询 $q_i^{(\mathrm{final})}$、场景上下文令牌 $c$ 和父节点文本嵌入 $t_{v_p}$：

$$t_{\mathrm{new}} = f([q_i^{(\mathrm{final})}; c; t_{v_p}]) \quad \text{(Eq. 9)}$$

3. **缓冲-聚类注册**：合成嵌入进入缓冲区，当 $M$ 个嵌入的成对相似度超过阈值 $\tau = 0.7$ 时，创建新类别节点，其文本嵌入为均值，视觉键继承自父节点：

$$v_{\mathrm{new}} \gets \{ t_{\mathrm{new}} = \frac{1}{M}\sum_{i=1}^{M} t_i, e_{\mathrm{new}} = e_{v_p}, p(v_{\mathrm{new}}) = v_p \} \quad \text{(Eq. 10)}$$

### 训练目标

HSGDet 的总损失由三部分加权组成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{det}} + \lambda_1 \mathcal{L}_{\mathrm{hier}} + \lambda_2 \mathcal{L}_{\mathrm{CR2T}} \quad \text{(Eq. 11)}$$

其中 $\lambda_1 = 0.5$，$\lambda_2 = 0.3$。$\mathcal{L}_{\mathrm{det}}$ 为标准检测回归损失。

**层次导航损失** $\mathcal{L}_{\mathrm{hier}}$ 监督目标类在层次路径上的所有祖先节点都应获得高注意力，以保持路径一致性：

$$\mathcal{L}_{\mathrm{hier}} = -\frac{1}{N_{\mathrm{gt}}} \sum_{i=1}^{N_{\mathrm{gt}}} \sum_{v \in \mathcal{P}(c_i)} \log \beta_{i,v} \quad \text{(Eq. 12)}$$

**CR2T 对比损失** 是防止合成嵌入坍塌到单一向量的关键机制，迫使生成嵌入靠近真实文本嵌入、远离负样本嵌入：

$$\mathcal{L}_{\mathrm{contrast}}^{i} = \max (0, \cos(t_i^{\mathrm{pred}}, t_i^{\mathrm{neg}}) - \cos(t_i^{\mathrm{pred}}, t_i^{\mathrm{gt}}) + \gamma) \quad \text{(Eq. 14)}$$

消融实验证实，移除对比损失会导致嵌入质量显著下降，验证了其在防止语义坍塌中的核心作用。

### 补充图表

![[assets/figures/papers/paper_list_l2336_https_openaccess_thecvf_com_content_CVPR2026_html_Azeem_Prompt_Free_Unkn/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of OVD and OWOD paradigms on a aerial scene with prompted classes (“car” and “house”) and an unprompted object (“lamp”). (a) OVD detects only prompted categories. (b) OWOD identifies novel classes as “unknown.” (c) Unified OW-OVD detects the prompted classes but flags “lamp” as “unknown”. (d) HSGDet autonomously discovers and labels it as “lamp” via contextual reasoning*



## 实验与关键发现

### 核心性能突破

HSGDet 在遥感开放世界检测的三个核心指标上均实现了对现有最佳方法的显著超越。在 DOTA-v2 基准上（Table 3），完整 HSGDet 取得了 **54.8 K-mAP**（已知类平均精度）、**41.2 U-R**（未知类召回率）和 **5.8 WI**（Wilderness Impact，即未知对象被误判为已知类的比例）。相较于此前最强的统一开放词汇-开放世界检测框架 **OW-OVD**（Xi et al., CVPR 2025），K-mAP 提升 **+6.6 点**，U-R 提升 **+9.9 点**，WI 降低 **36%**（从 9.1 降至 5.8）。这一结果验证了核心洞察：通过层次语义图上的场景条件化分类（DHGA）与上下文感知的区域到文本嵌入合成（CR2T）的协同，模型不仅能更准确地发现未知对象，还能为其赋予有意义的语义标签，从而从根本上缓解了未知对象对已知类分类的干扰。

![[assets/figures/papers/paper_list_l2336_https_openaccess_thecvf_com_content_CVPR2026_html_Azeem_Prompt_Free_Unkn/figures/005_Table_3.jpg]]
*Table 3: Comparison of OWOD methods on DOTA v2*

在另外两个遥感基准 FAIR1M 和 DIOR 上（Table 4），HSGDet 同样保持了稳定的领先优势，分别取得 52.4/38.5/6.2 和 59.3/42.8/5.2 的三指标成绩。跨域泛化实验（Table 5）进一步表明，该方法在通用自然图像数据集 COCO 上同样有效，K-mAP 和 U-R 分别达到 81.3 和 78.8，说明层次语义图与场景上下文建模的策略并非遥感场景特化，而是具有普适的开放世界检测能力。

![[assets/figures/papers/paper_list_l2336_https_openaccess_thecvf_com_content_CVPR2026_html_Azeem_Prompt_Free_Unkn/figures/006_Table_4.jpg]]
*Table 4: Comparison of OWOD methods performance on FAIR1M and DIOR*

![[assets/figures/papers/paper_list_l2336_https_openaccess_thecvf_com_content_CVPR2026_html_Azeem_Prompt_Free_Unkn/figures/007_Table_5.jpg]]
*Table 5: Comparison of OWOD methods performance on COCO dataset. The comparison results are from OW-OVD [42]*

### 组件消融：各模块的因果贡献

Table 1 的逐步消融实验清晰揭示了各模块的独立贡献。基线模型（无 DHGA、无 SCT、无 CR2T）的 U-R 仅为 20.5，WI 高达 10.3。**添加 DHGA** 后，U-R 跃升 **+7.5 个百分点**至 28.0，WI 降至 8.7，这归因于层次语义导航使模型能够在粗粒度语义约束下更准确地识别未知查询——当查询在精细类别上的最大注意力低于阈值 $\tau_{\mathrm{unk}}=0.4$ 时，DHGA 能可靠地将其路由至 CR2T 而非强行分类。进一步**引入场景上下文令牌（SCT）**后，U-R 再提升 **+5.8 个百分点**至 33.8，WI 降至 7.4，证明全局共现模式聚合对区分前景未知对象与背景干扰具有关键作用。最终**加入完整 CR2T** 模块后，U-R 达到 41.2（较基线 +20.7），WI 降至 5.8，K-mAP 也从基线的 44.7 提升至 54.8（+10.1），表明为未知对象合成语义嵌入不仅提升了未知召回，还通过减少未知→已知的误分类反向增强了已知类的检测精度。

![[assets/figures/papers/paper_list_l2336_https_openaccess_thecvf_com_content_CVPR2026_html_Azeem_Prompt_Free_Unkn/figures/003_Table_1.jpg]]
*Table 1: Ablation study of HSGDet components on DOTA-v2. KmAP: Known mAP, U-R: Unknown Recall, WI: Wilderness Impact*

### CR2T 内部机制分析

Table 2 的 CR2T 内部消融揭示了合成嵌入质量的关键决定因素。以**文本对齐度（TA，即生成嵌入与真实 CLIP 文本嵌入的余弦相似度）**、**语义一致性（SMC，即同类未知对象的视觉特征类内相似度）**和**U-R** 为评价维度：

![[assets/figures/papers/paper_list_l2336_https_openaccess_thecvf_com_content_CVPR2026_html_Azeem_Prompt_Free_Unkn/figures/004_Table_2.jpg]]
*Table 2: CR2T ablation on DOTA-v2. Text Alignment (TA): cosine similarity to ground-truth CLIP embedding. Semantic Coherence (SMC): intra-class visual similarity. VF: Visual Features, SC: Scene Context, HP: Hierarchical Parent, VO: Visual Only, SC:Sibling Context, Full: Full CR2T*

- **仅使用视觉特征（VO）**：TA 仅 0.62，U-R 为 34.8，说明纯视觉信号缺乏足够的语义约束。
- **视觉特征 + 场景上下文（VF+SC）**：TA 提升至 0.71，U-R 升至 37.5，验证了场景共现信息对语义定位的辅助作用。
- **完整 CR2T（VF+SC+HP，即视觉特征、场景上下文、层级父节点）**：TA 达到 **0.79**，SMC 达到 **0.82**，U-R 达到 **41.2**。层级父节点嵌入的引入是性能跃升的关键——父节点提供了粗粒度的语义锚点（例如“交通工具”对于未知的“卡车”），约束了嵌入生成的方向，防止其偏离合理的语义空间。

此外，训练数据敏感性实验表明，在训练时**随机掩盖 30% 的已知类作为伪未知类**可在 CR2T 嵌入质量（TA 0.79）和 U-R 之间取得最优平衡。过低的掩盖率导致 CR2T 训练样本不足，过高则损害已知类的分类性能。对比损失（$\mathcal{L}_{\mathrm{contrast}}$）被证实对防止嵌入坍塌至关重要——若不施加该损失，CR2T 生成的嵌入会退化为单一向量，TA 和 U-R 均大幅下降。

### 与基线的全面对比

在 DOTA-v2 上（Table 3），HSGDet 相较所有基线方法均展现出压倒性优势。早期开放世界检测器如 **OW-DETR**（Gupta et al., CVPR 2022）和 **CAT**（Ma et al., CVPR 2023）的 U-R 分别仅为 14.7 和 16.2，WI 高达 12.5 和 11.8，这是因为它们仅能标记“未知”而无法利用语义信息区分未知与背景。**PROB**（Zohar et al., CVPR 2023）通过概率目标性建模将 U-R 提升至 21.3，但仍缺乏语义标注能力。**UC-OWOD**（Wu et al., ECCV 2022）引入未知分类头后 U-R 达到 25.8，但 WI 仍高达 10.2。**OW-OVD** 作为此前最优的统一框架，利用视觉-语言模型将 U-R 推至 31.3，但其仍依赖外部文本提示且无法为未知对象生成标签。HSGDet 通过 DHGA 的场景条件化层次导航与 CR2T 的自主嵌入合成，首次实现了**无需外部提示的未知对象检测与语义标注一体化**，在三个指标上均大幅领先。

### 定性分析

Figure 3 的定性对比直观展示了 HSGDet 的核心优势。在 DOTA-v2 的航拍场景中，**OWOBJ**（Zhang et al., CVPR 2025）能够检测到未见过的新对象，但仅能将其标记为通用的“unknown”，无法提供任何语义信息。相比之下，HSGDet 不仅检测到同一对象，还通过 CR2T 的上下文推理赋予其具体类别标签（如“lamp”）。这一差异源于 CR2T 的三重信息融合机制：视觉查询提供对象的表观特征，场景上下文令牌注入全局共现模式（例如“lamp”常与“street”场景共现），层级父节点嵌入提供语义锚定（例如“lamp”在 WordNet 中的父节点“artifact”约束了嵌入方向）。

![[assets/figures/papers/paper_list_l2336_https_openaccess_thecvf_com_content_CVPR2026_html_Azeem_Prompt_Free_Unkn/figures/008_Figure_3.jpg]]
*Figure 3: Comparison between OWOBJ and HSGDet on DOTA-v2. OWOBJ detects the unseen objects without semantic grounding, whereas HSGDet detect the unseen object with proper class labels*

### 失败模式与局限性

尽管 HSGDet 在主要指标上表现优异，分析中仍存在若干值得关注的边界情况。首先，CR2T 的缓冲-聚类扩展策略依赖超参数（缓冲区大小 $M=5$，相似度阈值 $\tau=0.7$），这些参数在当前遥感场景下经过验证，但在类别密度极高或极低的场景中可能需要重新校准，否则可能导致过度合并或碎片化。其次，模型对 WordNet 层次先验的依赖意味着在完全不具备此类结构化知识的领域（如细粒度工业缺陷检测），初始语义图的构建策略需要重新设计。此外，连续未知类别扩展是否会引起类别间语义混淆或嵌入漂移，以及是否需要定期重新校准语义图，尚缺乏长周期部署的实验验证。CR2T 生成的语义嵌入在下游任务（如图像描述、视觉问答）中的有效性也仍有待探索。这些边界情况在当前论文中未被充分覆盖，需要在实际部署前进行手动验证。



## 定位与知识库关联

### 1. 问题定位：从“检测未知”到“命名未知”的范式跃迁

开放世界目标检测（OWOD）的核心挑战在于同时完成两项任务：识别已知类别，并发现训练时未见过的未知类别。现有方法在“发现未知”上已取得显著进展，但在“理解未知”上存在根本性瓶颈——所有主流方法只能将未知对象标记为匿名标签“unknown”，无法赋予任何语义信息。

这一瓶颈的根源在于分类策略的设计。**OW-DETR**（Gupta et al., CVPR 2022）、**CAT**（Ma et al., CVPR 2023）、**PROB**（Zohar et al., CVPR 2023）等方法依赖标准线性分类头，其输出空间被固定为已知类别加一个“unknown”类，本质上不具备语义扩展能力。**UC-OWOD**（Wu et al., ECCV 2022）虽然引入了专门的未知分类头，但仍停留在“检测到未知”层面。更近期的**OW-OVD**（Xi et al., CVPR 2025）试图统一开放词汇检测（OVD）与OWOD，但其对未知对象的处理仍然是将其标记为“unknown”，并未生成语义标签。**SkySense-O**（Zhu et al., CVPR 2025）面向遥感场景引入了视觉-语言模型，但依赖外部提示来指定检测目标。**OWOBJ**（Zhang et al., CVPR 2025）通过目标性建模统一新物体检测，同样止步于“unknown”标签。

HSGDet的核心贡献在于填补了这一空白：**首次实现了无需外部提示的未知对象自主命名**。这一能力使得开放世界检测从“检测到某物”跃迁到“检测到并理解某物”，对遥感监测等需要全自主部署的任务具有关键意义。

### 2. 方法谱系中的技术定位

#### 2.1 分类策略的演进：从线性头到场景条件化层次图注意力

| 方法 | 分类机制 | 语义输出 | 场景感知 |
|------|---------|---------|---------|
| OW-DETR / CAT / PROB | 线性分类头 | 已知类 + “unknown” | 无 |
| UC-OWOD | 线性头 + 未知分类头 | 已知类 + “unknown” | 无 |
| OW-OVD | 文本提示匹配 | 已知类 + “unknown” | 无 |
| **HSGDet (DHGA)** | 层次语义图上的可变形图注意力 | 已知类 + 语义标签 | 场景上下文令牌 |

HSGDet的DHGA模块在三个维度上实现了突破：

- **层次化导航**：不同于扁平分类空间，DHGA在基于WordNet IS-A关系构建的层次语义图上执行粗到细的分类。通过Top-K节点采样（基于查询与可学习键的相似度）和层次路径监督（见Eq. 12的层次导航损失），模型学会了沿语义树逐步缩小分类范围。
- **场景条件化**：引入可学习的场景上下文令牌（SCT），通过交叉注意力聚合所有查询的共现信息，为每个查询注入全局场景线索。这使分类不再是孤立的目标识别，而是场景感知的推理过程。
- **可学习键的自适应路径选择**：不同于固定的图结构遍历，DHGA通过可学习键嵌入实现自适应的语义路径选择，使模型能根据场景上下文动态调整分类粒度。

#### 2.2 未知对象处理：从匿名标记到语义嵌入合成

| 方法 | 未知对象输出 | 外部依赖 | 词汇扩展 |
|------|------------|---------|---------|
| 所有基线方法 | “unknown”标签 | 无 | 不支持 |
| 外部语言模型方案 | 语言模型生成的文本 | 外部LLM | 可能支持 |
| **HSGDet (CR2T)** | CLIP文本嵌入 | 无 | 缓冲-聚类自动扩展 |

CR2T模块的核心创新在于**在不依赖外部语言模型的情况下合成语义嵌入**。其输入融合了三个信息源：
1. **视觉特征**：最终精化的目标查询 $q_i^{(\mathrm{final})}$
2. **场景上下文**：场景上下文令牌 $c$
3. **层次父节点信息**：在采样节点中注意力权重最高的父节点文本嵌入 $t_{v_p}$

这三者的融合（Eq. 9）使CR2T生成的嵌入既保留了视觉特异性，又继承了层次语义结构，同时融入了场景共现模式。消融实验（Table 2）证实了每个信息源的必要性：仅使用视觉特征的变体（VO）在文本对齐（TA）上显著下降；移除场景上下文（无SC）导致语义一致性（SMC）降低；移除层次父节点（无HP）则削弱了语义结构的继承性。

#### 2.3 与开放词汇检测（OVD）的关系

HSGDet与OVD方法（如OW-OVD）的关键区别在于：OVD需要用户在推理时提供目标类别的文本提示，本质上是一个“提示→检测”的匹配过程；而HSGDet的CR2T模块是“检测→命名”的生成过程。这使得HSGDet能够发现提示中未包含的类别，而OVD只能检测用户指定的类别。Figure 1清晰地展示了这一差异：在包含“car”和“house”提示的航拍场景中，OVD忽略了未提示的“lamp”，而HSGDet自主发现并将其标注为“lamp”。

### 3. 适用边界与局限

#### 3.1 层次先验依赖

HSGDet的语义图初始结构基于WordNet的IS-A关系构建。在遥感场景中，WordNet覆盖了常见地物类别，但在以下场景中可能失效：
- **领域特定类别**：如特定型号的军事装备、专业遥感分类体系中的细粒度类别，可能不在WordNet中
- **非层次化类别体系**：某些应用场景的类别体系可能不具有清晰的IS-A层次结构
- **跨语言场景**：非英语词汇的语义层次可能与WordNet不匹配

**需要手动验证**：论文未讨论在完全不具有WordNet等层次先验的领域如何构建初始语义图，这是实际部署中的关键限制。

#### 3.2 缓冲-聚类扩展的敏感性

CR2T的词汇扩展依赖缓冲-聚类机制：当缓冲区中M个嵌入的成对相似度超过阈值τ时，创建新类别节点。论文默认设置为M=5, τ=0.7。这一机制在以下情况下可能不稳定：
- **类别密度不均**：在类别密集的场景中，不同类别的嵌入可能难以通过固定阈值区分
- **罕见类别**：出现频率极低的类别可能永远无法积累足够的缓冲样本
- **连续扩展的漂移**：随着语义图持续扩展，新加入的节点可能引入语义混淆或嵌入漂移

**开放问题**：论文未分析连续未知类别扩展是否会引起类别间语义混淆，以及是否需要定期重新校准语义图。

#### 3.3 共现模式学习的偏差风险

DHGA的场景条件化分类依赖从训练数据中学习的空间共现模式。在遥感场景中，这可能导致：
- **场景偏差**：如果训练数据中某些类别只在特定场景中共现（如“船”只与“水”共现），模型可能对场景外出现的该类别产生误判
- **罕见共现模式的遗漏**：极罕见的类别组合可能无法被有效学习

### 4. 知识库定位与后续工作方向

HSGDet在以下知识节点上建立了连接：

- **上游**：Deformable DETR（检测架构）、CLIP（视觉-语言先验）、Deformable Graph Attention（图注意力机制）、WordNet（语义层次结构）
- **平行**：OWOD系列方法（OW-DETR, CAT, PROB, UC-OWOD, OW-OVD, OWOBJ）、遥感视觉-语言模型（SkySense-O）
- **下游潜力**：HSGDet生成的语义嵌入理论上可用于更复杂的下游任务（如图像描述、视觉问答），但论文未进行验证

**关键开放问题**：
1. CR2T生成的语义嵌入在更复杂的下游任务中是否仍然有效？
2. 模型对遥感图像中极罕见类别的泛化性能如何？
3. 缓冲-聚类扩展策略的超参数在不同场景和类别密度下是否仍是最优？
4. 连续词汇扩展是否会导致嵌入空间的语义漂移，是否需要定期重新校准？

HSGDet的核心贡献在于证明了“无需外部提示的未知对象自主命名”是可行的，其技术路线——层次语义图导航+上下文感知嵌入合成——为开放世界检测的下一阶段发展提供了明确方向。后续工作需要在层次先验的自动化构建、扩展机制的鲁棒性、以及生成嵌入的下游任务验证等方向上进行深入探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/Prompt_Free_Unknown_Label_Generation_for_Open_World_Detection_in_Remote_Sensing.pdf]]
