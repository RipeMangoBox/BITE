---
title: HIMO A New Benchmark for Full Body Human Interacting with Multiple Objects
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objects.pdf
project_link: https://lvxintao.github.io/himo
code_link: null
aliases:
- HGHS
- HNBFBHIMO
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入大规模多物体交互数据集 HIMO，提供详细的文本描述和时域分割标注，使模型能够学习多物体间的时空协调与长序列的时序组合。
primary_logic: 采用双分支扩散模型结合互注意模块来解耦生成人体与物体运动，同时利用物体对损失约束物体间空间关系；并为多步交互设计自回归生成流水线，通过过去帧条件化实现平滑的交互片段过渡。
claims:
- HIMO dataset provides 3.3K 4D HOI sequences with 2-3 objects, temporally segmented and annotated with fine-grained text, enabling novel tasks.
- The mutual interaction module is critical; removing it causes a huge drop in R-precision (e.g., from 0.6369 to 0.4710 on 2-objects).
- Object-pairwise loss significantly improves motion plausibility; the ablation 'w/o dis' leads to degraded metrics.
- Conditioning on 10 past frames achieves best trade-off for HIMO-SegGen, yielding FID 4.2004 and highest R-precision.
---

# HIMO A New Benchmark for Full Body Human Interacting with Multiple Objects

> [!tip] 核心洞察
> 采用双分支扩散模型结合互注意模块来解耦生成人体与物体运动，同时利用物体对损失约束物体间空间关系；并为多步交互设计自回归生成流水线，通过过去帧条件化实现平滑的交互片段过渡。

| 字段 | 内容 |
|------|------|
| 中文题名 | HIMO：一个面向全身人体与多物体交互的新基准 |
| 英文题名 | HIMO A New Benchmark for Full Body Human Interacting with Multiple Objects |
| 会议/期刊 | ECCV 2024 |
| Links | [Project](https://lvxintao.github.io/himo) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HIMO-Gen / HIMO-SegGen |
| Dataset | HIMO 2-objects partition, HIMO 3-objects partition |

> [!tip] 效果简介
> - HIMO 2-objects partition 上，FID ↓ 1.4811 (HIMO-Gen) vs 6.8457 (MDM) (-5.3646)；R-Precision Top 3 ↑ 0.6404 (HIMO-SegGen) vs 0.6052 (MDM) (+0.0352)。
> - HIMO 3-objects partition 上，R-Precision Top 3 ↑ 0.5350 (HIMO-Gen) vs 0.5025 (MDM) (+0.0325)；MM-Dist ↓ 5.0866 (HIMO-Gen) vs 6.3144 (MDM) (-1.2278)。

## 概要

现有的人-物交互（HOI）数据集与生成方法长期受限于单物体交互场景，缺乏面向多物体、多步骤协同操作的精细标注数据，导致模型难以合成时空协调的复杂交互序列。为此，本文提出了 **HIMO**，一个面向全身人体与多物体交互的大规模基准数据集，并基于此设计了双分支扩散生成框架 **HIMO-Gen** 及其自回归扩展 **HIMO-SegGen**。

HIMO 数据集包含 3,376 条 4D HOI 序列、9.44 小时与 4.08M 帧数据，覆盖 53 类日常物体与 2–3 个物体的组合交互，并提供了细粒度的文本描述与时域分割标注（Table 1）。在方法层面，HIMO-Gen 采用双分支条件扩散模型，通过互注意模块实现人体与物体运动的解耦生成与特征融合，同时引入物体对损失约束多物体间的空间关系；HIMO-SegGen 则进一步构建自回归生成流水线，以过去 10 帧为条件实现多步交互片段的平滑过渡。

实验表明，在 2 物体分区上，HIMO-Gen 的 FID 降至 1.4811，显著优于 MDM 的 6.8457；在 3 物体分区上，R-Precision Top 3 达到 0.5350，MM-Dist 降至 5.0866。消融研究证实，互注意模块与物体对损失对生成质量至关重要——移除互注意模块后，2 物体分区的 R-Precision Top 3 从 0.6369 骤降至 0.4710。该工作为多物体 HOI 合成建立了数据基础与生成范式，但当前仍局限于 MoCap 模态，对未见物体几何的泛化存在接触缺陷，且自回归过渡机制缺乏自适应策略。



### 人-物交互生成：从单物体到多物体的范式跃迁

生成自然、协调的人与物体交互（Human-Object Interaction, HOI）运动序列，是计算机视觉与图形学中长期存在的核心挑战。其应用涵盖机器人学习、虚拟现实、动画制作等领域。然而，现有研究长期受困于一个根本性瓶颈：**人-物交互数据集普遍局限于单物体场景，缺乏多物体交互的精细标注数据**。这导致模型无法有效学习多物体间的时空协调关系，更无法合成复杂、多步骤的交互序列。

这一瓶颈的根源在于数据采集与标注的双重困难。多物体交互场景要求同时捕捉全身人体运动、手部精细动作以及多个物体的六自由度位姿，并在时间维度上对齐。此外，交互过程往往涉及顺序依赖——例如“先拿起杯子，再倒入水壶中的水，最后放下杯子”——这要求标注不仅描述“做什么”，还要精确刻画“何时做”以及“与哪个物体做”。现有数据集如GRAB、BEHAVE等虽然在单物体抓取或人-场景交互上取得进展，但在多物体、时域分割、细粒度文本描述三个维度上均存在显著缺口（见表1）。

### 现有方法的局限性

从生成方法的角度看，当前主流的运动生成模型同样暴露出对多物体交互场景的不适应。以**MDM**为代表的单分支扩散模型，将人体运动视为单一模态进行建模，缺乏对物体运动轨迹的显式推理能力。以**priorMDM**为代表的双人运动生成方法，虽然引入了多分支结构，但其交互建模仅限于人体-人体对，无法直接迁移至人体-多物体的异构交互场景。以**IMoS**为代表的意图驱动HOI合成方法，虽然考虑了交互目标，但仍局限于单物体设定，无法处理物体间的空间约束与操作顺序。

这些方法的共同缺陷可归纳为三个层面：
1. **架构层面**：缺乏解耦的人体-物体运动生成分支，导致两类运动模态的耦合不充分；
2. **约束层面**：没有显式的物体间关系损失，无法保证多个交互物体之间的空间一致性；
3. **时序层面**：仅支持单段文本引导的完整序列生成，无法应对多步骤交互中的片段过渡与长程时序组合。

### 本文的核心动机与设计思路

针对上述双重缺口，本文的工作围绕两条主线展开：

**主线一：构建大规模多物体交互基准数据集 HIMO。** HIMO包含3,376个HOI序列（总计9.44小时、4.08M帧），涵盖53类日常物体和34位受试者。其关键创新在于：每个序列涉及2-3个物体的协同交互，并配有细粒度的文本描述（明确交互顺序、操作模式和涉及的身体部位）以及时域分割标注。这使得HIMO成为首个同时支持“多物体交互生成”和“多步骤交互序列合成”任务的基准。

**主线二：设计专用于多物体HOI生成的双分支扩散框架。** 该框架的核心洞察是：**人体运动与物体运动应被解耦建模，但通过互注意机制实现深层特征融合；同时，物体间的空间关系需要显式损失函数约束。** 具体而言，方法包含三个关键设计：
- **双分支扩散模型**：人体分支与物体分支分别基于文本条件和初始状态生成各自的运动序列，互注意模块（Mutual Interaction Module）通过交叉注意力实现跨模态信息融合，确保人-物运动的时空对齐；
- **物体对损失**：基于交互物体几何中心之间的相对距离构建损失函数，显式约束生成结果中物体间的空间关系与真值一致；
- **自回归生成流水线**：将长序列分解为多个交互片段，以前一片段的末尾若干帧（经验最优为10帧）为条件生成下一片段，实现平滑的片段过渡与多步骤时序组合。

通过数据与方法的协同设计，HIMO基准为多物体HOI生成提供了标准化的评估平台，而HIMO-Gen/HIMO-SegGen框架则为这一新任务提供了具有竞争力的基线方案。



## 核心方法与创新机理

HIMO 的核心创新围绕“多物体、长序列、全身交互”这一未被现有基准覆盖的生成难题展开，可归纳为三个相互耦合的 changed slots。

### 1. 双分支扩散架构与互注意融合

现有方法（如 MDM）普遍采用单分支扩散模型，将人体与物体运动视为一个整体进行生成。这种做法在多物体交互场景下难以解耦不同实体的运动特性，导致生成质量下降。HIMO-Gen 提出**双分支条件扩散模型**，分别为人体运动（SMPL-X 参数）和物体运动（基于 BPS 几何表示）设立独立分支，并在每个 Transformer 层中嵌入**互注意模块**（Mutual Interaction Module）实现特征融合。

具体而言，互注意模块通过交叉注意力机制，使人体分支的 Query 查询物体分支的 Key-Value 对，反之亦然：

$$\pmb{H}^{(i+1)} = FF(softmax(\frac{\mathbf{Q}_h \mathbf{K}_o^T}{\sqrt{C}} \mathbf{V}_o)); \quad \pmb{O}^{(i+1)} = FF(softmax(\frac{\mathbf{Q}_o \mathbf{K}_h^T}{\sqrt{C}} \mathbf{V}_h))$$

这一设计的因果作用是**强制人体与物体在特征空间中进行双向信息交换**，从而保证生成的运动在时空上协调一致。消融实验提供了决定性证据：去除互注意模块后，2 物体分区的 R-Precision Top 3 从 0.6369 骤降至 0.4710（Table 4），降幅远超其他消融项，表明该模块是生成质量的关键瓶颈。

### 2. 物体对相对距离损失

单分支模型或未显式建模物体间关系的双分支模型，在多物体场景下容易出现物体间空间关系紊乱的问题。HIMO-Gen 引入**物体对损失**（object-pairwise loss），直接约束交互物体间的相对距离：

$$\mathcal{L}_{dis} = \sum_{i \neq j} \| \Delta V_{ij} - \Delta \hat{V}_{ij} \|_{2}^{2}$$

其中 $\Delta V_{ij}$ 和 $\Delta \hat{V}_{ij}$ 分别表示生成结果与真值中物体 $i$ 与 $j$ 的相对位移向量。该损失以权重 $\lambda_{dis}=0.1$ 加入总损失函数：

$$\mathcal{L} = \lambda_{vel} \mathcal{L}_{vel} + \lambda_{pos} \mathcal{L}_{pos} + \lambda_{pen} \mathcal{L}_{pen} + \lambda_{dis} \mathcal{L}_{dis}$$

消融实验（Table 4）显示，移除该损失（w/o dis）导致多项指标下降，论文文本分析明确指出其“在约束生成运动方面帮助很大”。这一设计的深层价值在于：它不依赖物体类别标签或预定义交互模板，而是通过纯几何约束实现物体间空间关系的保真，为开放场景下的多物体交互生成提供了可泛化的解决方案。

### 3. 自回归多步生成流水线

长序列多步交互的生成面临两个挑战：单次生成整段序列导致时序细节丢失；分段生成则存在片段间过渡不自然的问题。HIMO-SegGen 设计了**自回归生成流水线**，将长序列按文本描述的时间分割点拆分为多个片段，以前一片段的最后若干帧为条件生成下一片段。

该流水线的核心 knob 是**条件帧数**的选择。Table 5 的消融研究表明，使用 10 帧作为条件在 FID（4.2004）、R-Precision 和 MM-Dist 上均达到最佳，验证了“10 帧能最好地平衡上下文信息与过渡平滑性”这一经验发现。过多帧数可能引入冗余约束，过少则不足以捕捉运动连续性——这一非单调关系暗示存在一个信息瓶颈，10 帧恰好捕捉了人体运动的基本动力学状态。

值得注意的是，连续生成方案（非双分支）的性能大幅下降（论文文本消融描述，置信度 0.85），从反面验证了“分步生成 + 互注意设计”的必要性：单纯增加序列长度而不解耦人-物运动，无法有效应对多步交互的复杂性。

### 创新点之间的耦合关系

上述三个 changed slots 并非孤立设计，而是形成了一条因果链：**双分支架构**提供了人-物解耦的表示空间，**互注意模块**保证了该空间中的信息对齐，**物体对损失**约束了多物体间的空间一致性，而**自回归流水线**则将这一框架从单步交互扩展到多步长序列。任一环节的缺失都会导致性能显著下降，这从消融实验中各模块独立移除后的指标退化幅度可以得到印证。



HIMO-Gen 的整体生成框架围绕“解耦-融合-组合”三条主线构建，旨在从文本描述和初始状态出发，合成全身人体与多物体协调交互的 4D 运动序列。其核心设计动机源于一个关键瓶颈：单分支扩散模型难以同时捕捉人体运动与多物体运动的时空耦合关系，尤其在物体间存在功能关联（如“拿起杯子-倒水”）时，缺乏显式的物体间空间约束。

### 双分支条件扩散架构

框架的主体是一个双分支条件扩散模型（Fig. 4），分别处理人体运动和物体运动两种异质模态：

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/005_Figure_4.jpg]]
*Figure 4: Overview of the HOI synthesis framework. We propose a dual-branch conditional diffusion model to generate the human motion and object motions, respectively, conditioned on the textual description and the initial states of the human and objects. A mutual interaction module is also integrated for information fusion to generate coordinated HOI results*

- **Human Motion Branch（人体运动分支）**：以文本描述和人体初始姿态（SMPL-X 参数）为条件，生成全身人体运动序列。该分支需要同时建模身体、手部和手指的精细运动。
- **Object Motion Branch（物体运动分支）**：以物体几何形状（BPS 表示）和初始位姿为条件，生成多个物体的刚体运动轨迹。每个物体独立编码，但共享同一条件文本。

两个分支在扩散去噪过程中并行运行，但并非完全独立。框架在两个分支的 Transformer 层之间插入了 **Mutual Interaction Module（互注意模块）**，通过交叉注意力机制实现信息融合：

$$ \pmb{H}^{(i+1)} = FF(softmax(\frac{\mathbf{Q}_h \mathbf{K}_o^T}{\sqrt{C}} \mathbf{V}_o)) $$
$$ \pmb{O}^{(i+1)} = FF(softmax(\frac{\mathbf{Q}_o \mathbf{K}_h^T}{\sqrt{C}} \mathbf{V}_h)) $$

其中 $\pmb{H}$ 和 $\pmb{O}$ 分别为人体和物体的隐藏特征，$\mathbf{Q}_h$ 由人体特征产生，$\mathbf{K}_o$ 和 $\mathbf{V}_o$ 由物体特征提供，反之亦然。这一设计使人体分支能够“感知”物体的当前位置和运动趋势，物体分支也能“理解”人体的操作意图，从而保证生成的人-物交互在时空上协调一致。消融实验证实，移除该模块会导致 R-Precision Top 3 从 0.6369 骤降至 0.4710（Table 4），表明互注意是生成质量的关键因果节点。

### 多物体空间约束：物体对损失

在多物体交互场景中，物体之间的相对空间关系（如一只手同时持握两个物体时的距离模式）是交互合理性的重要指标。基线方法通常只关注人-物关系，忽略了物体-物体之间的空间依赖。HIMO-Gen 引入 **Object-pairwise Loss（物体对损失）** 来填补这一空白：

$$ \mathcal{L}_{dis} = \sum_{i \neq j} \| \Delta V_{ij} - \Delta \hat{V}_{ij} \|_{2}^{2} $$

该损失约束生成结果中任意两个交互物体间的相对距离向量 $\Delta V_{ij}$ 与真值 $\Delta \hat{V}_{ij}$ 保持一致。消融实验（Table 4 中 'w/o dis' 行）表明，移除该损失会导致多项指标退化，验证了物体间距离约束对于运动合理性的贡献。

### 整体优化目标

框架的最终优化目标由四个损失项加权组合而成：

$$ \mathcal{L} = \lambda_{vel} \mathcal{L}_{vel} + \lambda_{pos} \mathcal{L}_{pos} + \lambda_{pen} \mathcal{L}_{pen} + \lambda_{dis} \mathcal{L}_{dis} $$

其中：
- $\mathcal{L}_{pos}$（关节位置损失）和 $\mathcal{L}_{vel}$（关节速度损失）约束人体运动与真值的一致性；
- $\mathcal{L}_{pen}$（穿透损失）基于修正的 SDF 函数 $\phi(x,y,z) = -\min(SDF(x,y,z), 0)$，惩罚人体与物体的相互穿透；
- $\mathcal{L}_{dis}$（物体对损失）约束物体间相对距离。

经验权重设置为 $\lambda_{vel} = \lambda_{pos} = \lambda_{pen} = 1$，$\lambda_{dis} = 0.1$。

### 多步骤交互的自回归生成流水线

对于包含多个时序步骤的长序列交互（如“先拿起杯子，再倒水，最后放下”），单次生成整段序列难以保证各步骤的精确时序控制。为此，框架设计了 **HIMO-SegGen 自回归生成流水线**（Fig. 5）：

1. 将长序列按文本描述的时间分割点分解为多个片段；
2. 首片段由初始状态和文本条件生成；
3. 后续每个片段的生成以前一片段的最后 $k$ 帧为条件，通过将过去帧的位姿信息注入扩散模型的输入，实现片段间的平滑过渡。

条件帧数 $k$ 是一个关键超参数。消融实验（Table 5）表明，$k=10$ 在 FID（4.2004）、R-Precision 和 MM-Dist 上均达到最优，在提供足够时序上下文与保持过渡平滑性之间取得了最佳平衡。过少的帧数导致过渡不连贯，过多的帧数则可能过度约束生成多样性。

### 输入输出流总结

**输入**：
- 文本描述（描述交互顺序、模式和涉及的身体部位）
- 人体初始姿态（SMPL-X 参数）
- 各物体的初始位姿和几何形状（BPS 表示）

**输出**：
- 全身人体运动序列（SMPL-X 参数序列）
- 多物体刚体运动轨迹（位姿序列）

**数据流**：文本经 CLIP 编码后作为全局条件注入两个分支；初始状态作为扩散模型的起点；双分支在去噪的每一步通过互注意模块交换信息；最终生成的参数序列可通过 SMPL-X 模型和物体网格渲染为可视化的 4D 交互序列（Fig. 6）。



### 双分支扩散生成架构

HIMO-Gen 的核心是一个**双分支条件扩散模型**，分别处理人体运动和物体运动。人体分支以文本描述和 SMPL-X 初始姿态为条件生成全身运动参数；物体分支以物体几何形状的基点点集（Basis Point Set, BPS）表示和初始位姿为条件，生成多个物体的运动轨迹。两条分支在扩散去噪过程中通过**互注意模块（Mutual Interaction Module）** 进行信息融合。

互注意模块的核心操作是交叉注意力：人体分支的查询向量 $\mathbf{Q}_h$ 从物体分支获取键-值对 $(\mathbf{K}_o, \mathbf{V}_o)$，物体分支的查询向量 $\mathbf{Q}_o$ 从人体分支获取键-值对 $(\mathbf{K}_h, \mathbf{V}_h)$，实现双向特征融合：

$$
\pmb{H}^{(i+1)} = \text{FF}\left(\text{softmax}\left(\frac{\mathbf{Q}_h \mathbf{K}_o^T}{\sqrt{C}}\right) \mathbf{V}_o\right)
$$

$$
\pmb{O}^{(i+1)} = \text{FF}\left(\text{softmax}\left(\frac{\mathbf{Q}_o \mathbf{K}_h^T}{\sqrt{C}}\right) \mathbf{V}_h\right)
$$

其中 $\pmb{H}^{(i+1)}$ 和 $\pmb{O}^{(i+1)}$ 分别为更新后的人体和物体隐层表示，$\text{FF}$ 为前馈网络，$C$ 为通道维度。该模块确保生成的人体运动与物体运动在时空上协调一致。消融实验表明，移除该模块后 2 物体分区的 R-Precision Top 3 从 0.6369 骤降至 0.4710（Table 4），验证了其关键作用。

### 损失函数设计

模型的总损失函数为四项损失的加权和：

$$
\mathcal{L} = \lambda_{vel} \mathcal{L}_{vel} + \lambda_{pos} \mathcal{L}_{pos} + \lambda_{pen} \mathcal{L}_{pen} + \lambda_{dis} \mathcal{L}_{dis}
$$

各权重经验设定为 $\lambda_{vel} = \lambda_{pos} = \lambda_{pen} = 1$，$\lambda_{dis} = 0.1$。

**位置损失** $\mathcal{L}_{pos}$ 约束生成的人体关节位置与真值一致：

$$
\mathcal{L}_{pos} = \frac{1}{N} \sum_{n=1}^{N} \sum_{j=1}^{J} \| P_{n}^{j} - \hat{P}_{n}^{j} \|_{2}^{2}
$$

其中 $N$ 为帧数，$J$ 为关节数，$P_{n}^{j}$ 和 $\hat{P}_{n}^{j}$ 分别为第 $n$ 帧第 $j$ 个关节的生成位置和真值位置。

**速度损失** $\mathcal{L}_{vel}$ 约束生成运动的时序动态与真值一致：

$$
\mathcal{L}_{vel} = \frac{1}{N-1} \sum_{n=1}^{N-1} \sum_{j=1}^{J} \| (P_{n+1}^{j} - P_{n}^{j}) - (\hat{P}_{n+1}^{j} - \hat{P}_{n}^{j}) \|_{2}^{2}
$$

**穿透损失** $\mathcal{L}_{pen}$ 惩罚物体穿入人体的现象。首先定义修正符号距离函数 $\phi(x,y,z) = -\min(\text{SDF}(x,y,z), 0)$，使得仅在人体内部取正值，外部为零。对每个物体表面采样 $S$ 个点 $v_{o}^{i}$，计算该物体的穿透度量：

$$
P_{o} = \sum_{i=1}^{S} \tilde{\phi}(v_{o}^{i})
$$

总穿透损失为所有交互物体的穿透度量之和：

$$
\mathcal{L}_{pen} = \sum_{o \in O} P_{o}
$$

**物体对距离损失** $\mathcal{L}_{dis}$ 约束交互物体之间的相对空间关系，确保多物体间的协调性：

$$
\mathcal{L}_{dis} = \sum_{i \neq j} \| \Delta V_{ij} - \Delta \hat{V}_{ij} \|_{2}^{2}
$$

其中 $\Delta V_{ij}$ 和 $\Delta \hat{V}_{ij}$ 分别为生成结果和真值中物体 $i$ 与物体 $j$ 之间的相对距离向量。消融实验（Table 4）显示，移除该损失（w/o dis）会导致多项指标下降，验证了物体间距离约束的有效性。

### 自回归生成流水线

针对多步骤交互的长序列生成，HIMO-SegGen 采用**自回归流水线**：将完整交互序列按文本描述的时域分割边界切分为多个片段，以前一片段的最后若干帧为条件生成下一片段。条件帧数通过实验确定：使用 10 帧作为条件在 FID (4.2004)、R-Precision 和 MM-Dist 上均达到最佳（Table 5），能够在上下文信息保留与片段间过渡平滑性之间取得最优平衡。

### 补充图表

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/006_Figure_5.jpg]]
*Figure 5: The auto-regressive generation pipeline. The auto-regressive pipeline to iteratively generate the HOI synthesis results. We obtain the subsequent motion conditioned on the last few frames of the previously generated motion*



## 实验与关键发现

### 主实验结果

在 HIMO 数据集的两个分区（2-objects 和 3-objects）上，HIMO-Gen 与 HIMO-SegGen 均显著优于现有基线方法。定量评估采用 FID、R-Precision、MM-Dist、Diversity 和 MModality 五项指标，并报告 95% 置信区间。所有基线方法均被重新实现以支持多物体几何和初始状态条件的输入，数据集划分遵循 HumanML3D 协议（训练/验证/测试比例为 0.8/0.05/0.15）。

在 2-objects 分区上（Table 2），HIMO-Gen 取得了 **1.4811** 的 FID，相较于单分支扩散模型 **MDM** 的 6.8457 下降了 5.3646，降幅达 78.4%。HIMO-SegGen 则在 R-Precision Top 3 上达到 **0.6404**，优于 MDM 的 0.6052。在 3-objects 分区上（Table 3），HIMO-Gen 的 R-Precision Top 3 为 **0.5350**，MM-Dist 降至 **5.0866**，而 MDM 分别为 0.5025 和 6.3144，MM-Dist 降幅约 19.4%。值得注意的是，HIMO-SegGen 在 3-objects 场景下的 FID 优势相对缩小，这提示自回归流水线在更复杂的多物体协调中可能面临误差累积的挑战。

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/007_Table_2.jpg]]
*Table 2: Quantitative baseline comparisons on the 2-objects partition of HIMO. ± indicates the 95% confidence interval and → means the closer the better. Bold indicates best result and underline indicates second best*

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/008_Table_3.jpg]]
*Table 3: Quantitative baseline comparisons on the 3-objects partition of HIMO*

与 **IMoS**（意图驱动的 HOI 合成）和 **priorMDM**（双人运动生成扩散模型）相比，HIMO-Gen 在所有指标上均保持领先。priorMDM 的双分支设计虽天然适合多主体生成，但由于缺乏互注意融合和物体对损失，其在物体运动协调性上明显弱于 HIMO-Gen。

### 消融实验

消融实验在 2-objects 分区上进行，系统验证了各模块的因果贡献（Table 4）。

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/010_Table_4.jpg]]
*Table 4: Ablation studies of several model designs on 2-objects partition of HIMO*

**互注意模块（Mutual Interaction Module）是关键瓶颈**。移除该模块后（w/o IM），R-Precision Top 3 从 0.6369 骤降至 0.4710，降幅达 26.1%。这表明人体与物体分支之间的交叉注意力融合对于生成时空对齐的协调交互不可或缺。单独运行人体分支或物体分支（连续生成方案）同样导致性能大幅下降，进一步验证了双分支解耦设计的必要性。

**物体对损失（Object-pairwise Loss）显著提升运动合理性**。移除该损失（w/o dis）后，多项指标出现退化。该损失通过约束交互物体间的相对距离与真值保持一致，有效防止了生成结果中物体相互穿透或脱离交互范围的问题。

**自回归流水线的上下文帧数存在最优值**。在 HIMO-SegGen 的消融中（Table 5），分别测试了 1、5、10、20、50 帧作为条件。结果显示 **10 帧达到最佳平衡**：FID 为 4.2004，R-Precision 和 MM-Dist 均优于其他设置。过少的帧数（如 1 帧）无法提供足够的上下文信息，导致片段间过渡不自然；过多的帧数（如 50 帧）则可能引入冗余约束，限制生成多样性。

### 泛化能力与失败模式

在未见物体几何形状上的泛化实验（Fig. B）表明，HIMO-Gen 能够为训练集未出现的新物体网格生成合理的交互运动，但人-物接触区域仍存在局部穿透或悬空缺陷。这暴露了当前基于 BPS 表示的几何感知能力的局限——模型更依赖物体整体形状而非精细的局部几何。

在新颖 HOI 组合上的泛化实验（Fig. C）中，模型对训练中未见的“动作-物体”配对展现出一定的组合泛化能力，但交互的自然度随组合新颖程度的增加而下降。

### 局限性与开放问题

当前方法存在三个主要局限：
1. **模态单一**：数据集仅包含 MoCap 数据，未覆盖 RGB 模态，限制了直接应用于视觉生成任务。
2. **几何感知不足**：对未见物体几何的泛化依赖 BPS 表示，缺乏精细的接触建模，需要引入基于物理的接触模型或更强大的几何编码器。
3. **过渡帧数依赖经验**：自回归流水线中的上下文帧数（10 帧）通过消融实验确定，缺乏理论依据或自适应选择机制。

开放问题包括：能否将流水线扩展至开放词汇的物体类别？如何与神经渲染技术结合以生成外观逼真的交互视频？这些方向有待后续工作探索。

### 补充图表

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/002_Table_1.jpg]]
*Table 1: Dataset comparisons. We compare the HIMO dataset with existing human-object interaction datasets. “Multi-object”, “Segment” and*

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/011_Table_5.jpg]]
*Table 5: Ablation studies of the frame number of conditioned frames for HIMO-SegGen on 2-objects partition of the HIMO dataset*

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/009_Figure_6.jpg]]
*Figure 6: Visualization results. Our HIMO-Gen framework can generate plausible and realistic sequences of human interacting with multiple objects*

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the HIMO capture system. (a). We combine the Optitrack MoCap framework and the inertial gloves as a hybrid MoCap system. (b). Some examples of the 3D printed objects and the attached reflective markers. (c). The whole HOI MoCap framework, where the objects, the human body and hands of the subject are spatially aligned, and the Optitrack and inertial gloves are temporally synchronized*

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/013_Figure.jpg]]
*Figure: Fig. A: Visualization of the distribution of object combinations. Fig. B: Generalization experiment on unseen object meshes*

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/014_Figure.jpg]]
*Figure: Fig. C: Generalization experiment on novel HOI compositions. The text in blue denotes the novel HOI action*

![[assets/figures/papers/paper_list_l1760_HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objec/figures/017_Figure.jpg]]
*Figure: Fig. F: Visualization results of HIMO-SegGen*



## 定位与知识库关联

### 1. 与基线方法的关系

HIMO-Gen / HIMO-SegGen 的核心贡献在于首次将人-物交互（HOI）生成从单物体场景拓展至多物体、多步骤的复杂交互序列。其方法设计直接回应了现有基线在三个维度上的不足：

- **单分支架构的局限**：现有方法如 **MDM**（单分支扩散运动生成）和 **priorMDM**（双人运动生成的扩散模型）均采用单分支扩散架构，无法显式解耦人体运动与物体运动。HIMO-Gen 提出双分支扩散模型，分别对人体（SMPL-X参数）和物体（BPS几何表示）建模，并通过**互注意模块**实现跨分支特征融合。消融实验表明，去除该模块后，2对象分区的 R-Precision Top 3 从 0.6369 骤降至 0.4710（Table 4），验证了双分支解耦设计的必要性。

- **物体间关系建模的缺失**：此前方法（如 **IMoS**，意图驱动的 HOI 合成）未显式约束多物体间的空间关系。HIMO-Gen 引入**物体对相对距离损失**（Eq. 12），强制生成结果中交互物体间的相对距离与真值一致。消融中去除该损失（w/o dis）导致多项指标下降，证明其对运动合理性的关键作用。

- **多步骤生成的空白**：现有基线仅支持单段文本引导生成完整序列，无法处理“先拿杯子，再倒水”这类时序组合指令。HIMO-SegGen 设计了**自回归生成流水线**，将长序列分解为片段，以前一段末尾帧为条件生成下一段，实现了多步骤交互的平滑过渡。

### 2. 适用边界与泛化能力

- **数据模态边界**：HIMO 数据集仅包含 MoCap 运动数据（SMPL-X参数 + 物体6D位姿），不包含 RGB 视频或深度图。因此，HIMO-Gen 生成的是**纯运动序列**，无法直接输出可渲染的外观信息。这使其适用于运动规划、仿真和动画驱动等任务，但限制了在视觉内容生成（如视频合成）中的直接应用。

- **物体几何泛化**：方法使用 BPS 表示编码物体几何形状，理论上可处理未见物体网格。实验显示，在未见物体几何上仍存在人-物接触缺陷（Fig. B），表明当前几何感知模块的泛化能力有限，需要更强的几何编码或物理接触模型。

- **物体类别封闭性**：HIMO 数据集包含预定义的 58 个物体类别（Table A），模型在这些类别内训练和评估。论文未验证向开放词汇物体类别的扩展能力，这构成一个明确的适用边界。

- **上下文帧数依赖**：自回归流水线的过渡平滑性依赖于条件帧数的经验选择（最佳为 10 帧，Table 5）。该参数缺乏自适应机制，在不同交互节奏或物体数量的场景下可能需要重新调优。

### 3. 局限与开放问题

论文明确指出的局限及由此衍生的开放问题包括：

- **物理真实感不足**：当前仅通过穿透损失（Eq. 9-11）和物体对距离损失约束交互，未引入基于物理的接触力学模型。这导致生成的抓取、放置等动作可能违反物理规律。一个关键开放问题是：**能否将基于物理的接触模型（如摩擦力、接触力）嵌入扩散生成框架，以提升交互的物理合理性？**

- **未见物体的接触缺陷**：对训练集外物体几何的泛化仍存在明显的穿透和接触不准问题。这指向一个开放方向：**是否需要引入显式的物体几何编码器（如 PointNet++ 或 Transformer-based 编码器）替代当前的 BPS 表示，以增强几何感知能力？**

- **仅限运动模态**：生成结果缺乏外观信息，限制了在视觉内容创作中的端到端应用。一个自然的延伸是：**如何将 HIMO-Gen 的运动输出与神经渲染技术（如 NeRF、3D Gaussian Splatting）结合，生成外观逼真的多物体交互视频？**

- **开放词汇扩展**：当前方法依赖预定义的物体类别和交互模板。**能否将文本条件扩展至开放词汇描述，使模型能够处理“拿起一个从未见过的工具并修理另一个物体”这类组合指令？** 这需要结合大规模语言-运动预训练模型。

### 4. 知识库定位

HIMO-Gen 在 HOI 生成领域的知识谱系中占据以下位置：

- **上游依赖**：继承了扩散模型在人体运动生成中的成功范式（源自 MDM 等工作的扩散架构），并借鉴了双人运动生成中的特征融合思路（如 priorMDM 的交叉注意力），但将其推广至人-物多体交互场景。

- **并行工作**：与同期关注 HOI 生成的工作（如 IMoS）相比，HIMO-Gen 的核心区分点在于**多物体协调**和**时序分割生成**，这两个维度在现有基准中均未被系统探索。

- **下游推动**：HIMO 数据集本身填补了多物体交互标注数据的空白（3.3K 序列，含 2-3 物体，细粒度文本和时域分割），为后续研究提供了基准。HIMO-Gen 的双分支架构和自回归流水线可作为未来多体交互生成任务的基线框架。



## 原文 PDF

![[paperPDFs/ECCV_2024/HIMO_A_New_Benchmark_for_Full_Body_Human_Interacting_with_Multiple_Objects.pdf]]
