---
title: "PCMG: Psychology-driven Personality-consistent Text-to-Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/PCMG_Psychology_driven_Personality_consistent_Text_to_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- PCMG
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将人格注入解耦为两个阶段：1）个性整合阶段（OCEAN-CN），利用残差架构在扩散主干中注入心理先验而不破坏语义；2）运动精化阶段（Laban-Gd），利用拉班运动分析（LMA）的分析梯度引导，在采样期间调整关节旋转，实现心理物理上的精确控制。
primary_logic: 通过两阶段设计，先在扩散模型的特征层面融合人格条件，再在运动空间通过可微的LMA能量函数引导采样轨迹，从而在保持语义准确性的同时显式地表达人格特质。
claims:
- PCMG在MoOCEAN数据集上显著优于基线方法，FID从5.7534降至3.7754，PRS从0.4877提升至0.6535。
- 消融实验表明移除OCEAN-CN导致FID增加37.38%，运动真实感显著下降；移除Laban-Gd则导致PRS明显降低。
- 用户研究中73.64%的参与者偏好完整模型而非没有Laban-Gd的变体，表明Laban-Gd有效增强人格表达。
- MoOCEAN 上 FID↓ = 3.7754
---

# PCMG: Psychology-driven Personality-consistent Text-to-Motion Generation

> [!tip] 核心洞察
> 通过两阶段设计，先在扩散模型的特征层面融合人格条件，再在运动空间通过可微的LMA能量函数引导采样轨迹，从而在保持语义准确性的同时显式地表达人格特质。

| 字段 | 内容 |
|------|------|
| 中文题名 | PCMG：心理学驱动的人格一致文本到运动生成 |
| 英文题名 | PCMG: Psychology-driven Personality-consistent Text-to-Motion Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2505.22637) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PCMG |
| Dataset | MoOCEAN |

> [!tip] 效果简介
> - MoOCEAN 上，FID↓ 3.7754 vs 5.7534 (MDM+Personality) (-1.9780 (34.4%))；R-precision (Top-3)↑ 0.3281 vs 0.2656 (MDM+Personality) (+0.0625)；PRS↑ (Personality Recognition Score) 0.6535 vs 0.4877 (MotionDiffuse+Personality) (+0.1658)。

## 概要

**核心问题**：现有文本到运动生成方法主要关注语义保真度，缺乏显式机制确保生成的动作与目标人格之间的心理一致性。简单的人格文本描述或黑盒风格编码无法捕捉人格的精细运动学特征，导致动作语义正确但缺乏可区分的个性。

**核心结论**：PCMG通过两阶段设计——先在扩散模型的特征层面融合人格条件（OCEAN-CN），再在运动空间通过可微的拉班运动分析（LMA）能量函数引导采样轨迹（Laban-Gd）——在保持语义准确性的同时显式地表达人格特质。

**方法定位**：PCMG属于心理学驱动的人格一致文本到运动生成框架，将人格注入解耦为个性整合与运动精化两个阶段。OCEAN-CN采用双分支残差架构，在冻结的MDM主干上注入心理先验而不破坏语义；Laban-Gd利用LMA的分析梯度引导，在采样后期调整关节旋转，实现心理物理上的精确控制。

**主要结果**：在MoOCEAN数据集上，PCMG的FID降至3.7754（较最佳基线MotionDiffuse+Personality的5.4670降低约30.9%），人格识别得分PRS从0.4877提升至0.6535。消融实验表明移除OCEAN-CN导致FID增加37.38%，移除Laban-Gd则使PRS明显下降；用户研究中73.64%的参与者偏好完整模型。



### 问题背景

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体动作序列，在虚拟角色动画、游戏开发和影视制作中具有广泛应用。近年来，基于扩散模型的方法在该领域取得了显著进展，能够生成语义准确且物理合理的运动。然而，这些方法主要关注**语义保真度**，即生成的动作是否与文本描述一致，却普遍忽略了一个关键维度——**人格一致性**。

人类动作不仅是语义内容的载体，更是表达个体人格特质的重要媒介。心理学研究表明，不同人格的个体在执行相同语义任务时会表现出可区分的运动学特征。例如，高外向性的人挥手时幅度更大、速度更快，而高神经质的人则可能表现出更拘谨的姿态。现有方法即使将人格描述词嵌入提示文本，生成的往往仍是“语义正确但人格中性”的动作——缺乏可区分的个性表达。

### 现有方法的局限

当前将人格信息注入运动生成流程的尝试主要存在两类缺陷：

**1. 文本注入的不可靠性。** 将人格描述直接写入文本提示（如“一个外向的人挥手”）看似直观，但语言模型对人格的运动学映射是隐式且不精确的。文本描述无法捕捉人格的精细运动学特征，导致生成的动作在人格维度上缺乏可区分性。

**2. 黑盒风格编码的粗糙性。** 将人格向量直接线性投影并注入扩散模型（如 **MDM+Personality** 和 **MotionDiffuse+Personality**）虽然避免了文本歧义，但这种粗暴的注入方式存在两个根本问题：其一，直接修改扩散主干可能破坏预训练模型的语义生成能力（灾难性遗忘）；其二，单一的特征融合无法显式控制具体的运动学参数（如关节旋转幅度、空间利用方式），导致人格表达停留在表面。

### 核心瓶颈

现有方法缺乏一种**显式机制**来确保生成的动作与目标人格之间的心理一致性。具体而言，瓶颈在于：

- **特征层面**：如何在注入人格先验的同时，不破坏扩散模型已有的语义生成能力？
- **运动层面**：如何将抽象的人格特质转化为可微的运动学约束，实现对关节旋转、空间利用等精细参数的显式控制？

### 本文动机与核心思路

针对上述瓶颈，PCMG 提出了一种**心理学驱动的两阶段人格注入框架**，将人格一致性解耦为两个互补的子问题：

1. **个性整合阶段（OCEAN-CN）**：在扩散模型的特征层面，采用双分支残差架构将心理先验注入冻结的扩散主干。通过零初始化层将人格分支的残差特征添加到预训练模型，既引入了人格条件，又避免了灾难性遗忘，确保语义生成能力不受损害。

2. **运动精化阶段（Laban-Gd）**：在扩散采样的后期，引入基于**拉班运动分析（LMA）**的分析梯度引导。LMA 是舞蹈与表演理论中描述人体运动表现力的经典框架，其 Effort 因子（Space、Weight、Time、Flow）与心理学中的 OCEAN 人格模型存在经实证验证的映射关系。Laban-Gd 利用这一映射，通过梯度下降在采样过程中调整关节旋转，实现心理物理层面上的精确控制。

这种两阶段设计的核心洞察在于：**先在特征层面融合人格条件以保持语义准确性，再在运动空间通过可微的 LMA 能量函数引导采样轨迹，从而显式地表达人格特质**。两个阶段各司其职——OCEAN-CN 负责“人格语义”的宏观注入，Laban-Gd 负责“人格运动学”的微观精化——共同实现了语义正确且人格鲜明的运动生成。



## 核心方法与创新机理

PCMG的核心创新在于将人格注入解耦为**语义层面的特征融合**与**运动学层面的分析性精化**两个阶段，从而在保持文本语义保真度的同时，显式地表达大五人格（OCEAN）特质。这一设计与现有基线方法形成了清晰的差异。

### 1. 从“黑盒注入”到“双分支残差融合”

现有基线方法普遍采用朴素的人格注入策略：**MDM+Personality**将人格向量线性投影后直接加到噪声运动中，**MotionDiffuse+Personality**则将人格向量注入动作隐空间。这类直接求和或拼接的方式将人格视为与文本嵌入同质的附加条件，容易在训练中引发灾难性遗忘——模型为了拟合人格信号而牺牲已学到的语义-运动映射。

PCMG提出的**OCEAN-CN（OCEAN ControlNet）**模块改变了这一范式。它采用双分支Transformer架构：冻结的MDM编码器主干保留原有的文本-运动生成能力，并行的可训练人格分支通过**零初始化线性层**将残差特征注入主干。零初始化的关键作用在于：训练初期人格分支输出为零，模型完全复用预训练MDM的行为；随着训练推进，人格分支逐渐学习到需要“修正”的特征残差，从而在不破坏语义的前提下叠加人格先验。消融实验直接验证了这一设计的必要性——移除OCEAN-CN后，FID从3.7754飙升至6.0288（+37.38%），表明运动真实感严重退化。

### 2. 从“隐式编码”到“拉班分析梯度引导”

即使人格特征被成功注入扩散模型的特征空间，生成的动作仍可能在运动学细节层面缺乏可区分的个性。这是因为扩散模型的去噪目标是最小化数据分布的距离，而非显式优化关节旋转与人格特质之间的心理物理学对应关系。

PCMG引入的**Laban-Gd（Laban Guidance）**模块直接针对这一瓶颈。它基于拉班运动分析（LMA）理论，将OCEAN人格向量映射为Space和Weight两个Effort因子的目标值，进而转换为具体关节的旋转方向约束（如Table I和Table II所示的旋转符号表）。在扩散采样的后期阶段（$t < T_G$），Laban-Gd通过梯度下降调整预测均值：

$$\pmb {\mu } _ { t } = \pmb {\mu } _ { t } - \tau \nabla _ { \pmb {\mu } _ { t } } G \left( \pmb {\mu } _ { t } , \pmb { c } ^ { p } \right)$$

其中差异函数$G$计算生成动作的全局坐标与人格一致目标坐标之间的加权L2距离。这种**分析性引导**将抽象的人格特质转化为可微的运动学约束，在采样轨迹上施加物理上可解释的修正。消融实验显示，移除Laban-Gd后PRS从0.6535降至0.6086，用户研究中73.64%的参与者偏好完整模型，表明该模块对人格表达有显著贡献。

### 3. 两阶段协同的因果机制

OCEAN-CN与Laban-Gd并非独立的改进，而是形成互补的因果链路：**OCEAN-CN负责“像不像这个人”——**在特征层面确保生成动作的整体风格与目标人格一致；**Laban-Gd负责“细节对不对”——**在运动学层面确保关节旋转符合该人格特质的心理物理学规律。前者通过残差融合保护语义，后者通过分析梯度注入运动学先验，两者共同解决了“语义正确但个性缺失”的核心瓶颈。



PCMG 的整体 pipeline 将人格注入解耦为两个阶段，形成“先融合、后精化”的级联架构。输入为文本提示 `p`、OCEAN 五维人格向量 `c` 和噪声运动序列 `x_t`，输出为与文本语义和人格特质双重一致的运动序列 `x_0`。

**阶段一：个性整合（OCEAN-CN）**。该阶段在扩散模型的特征层面注入心理先验。OCEAN-CN 采用双分支残差架构：冻结的 MDM Transformer 编码器作为主干，并行一个可训练的人格分支。人格分支接收 OCEAN 向量，通过零初始化线性层将残差特征逐层添加到主干的中间表示中。这种设计使得人格条件能够在不破坏预训练语义生成能力的前提下，逐步习得人格相关的运动模式。零初始化确保了训练初期人格分支输出为零，模型从纯语义生成平稳过渡到人格感知生成，有效避免了灾难性遗忘。

**阶段二：运动精化（Laban-Gd）**。该阶段在扩散采样的后期，通过可微的拉班运动分析（LMA）能量函数对关节旋转进行梯度引导。具体流程为：从 `t = T` 到 `t = T_G` 先进行粗粒度去噪，待运动结构基本成形后，在每一步采样前利用 Laban-Gd 调整预测均值 μ_t：

$$\pmb{\mu}_t = \pmb{\mu}_t - \tau \nabla_{\pmb{\mu}_t} G(\pmb{\mu}_t, \pmb{c}^p)$$

其中差异函数 `G` 度量生成运动的全局坐标 `R(μ)` 与人格一致目标坐标 `c^p` 之间的加权 L2 距离：

$$G(\pmb{\mu}, \pmb{c}^p) = \frac{\sum_n \sum_j \sigma_{nj} \left\| \pmb{c}^p - \pmb{R}(\pmb{\mu}) \right\|_2}{\sum_n \sum_j \sigma_{nj}}$$

`σ_nj` 为二进制掩码，指示当前人格维度所影响的关节。Laban-Gd 仅在后期采样步骤（`t < T_G`）生效——早期样本噪声过大，强行引导会导致脚步滑动等非自然现象；而一旦运动结构清晰后，分析性引导便能精确调整关节旋转，使动作在心理物理层面符合目标人格特征。

**模块间的因果分工**：OCEAN-CN 负责在语义生成过程中建立人格与运动模式的全局关联，Laban-Gd 则在运动空间中对局部运动学细节进行精细校准。消融实验验证了这一分工的有效性——移除 OCEAN-CN 导致 FID 从 3.7754 升至 6.0288（+37.38%），运动真实感急剧下降；移除 Laban-Gd 则使 PRS 从 0.6535 降至 0.6086，人格可辨识度明显减弱。两者协同实现了“语义准确”与“个性鲜明”的双重目标。



PCMG将人格注入解耦为两个阶段：**个性整合**与**运动精化**，分别在扩散模型的特征层面和运动空间的操作层面施加控制，从而在保持语义准确性的同时显式地表达人格特质。

### 个性整合：OCEAN-CN

OCEAN-CN（OCEAN ControlNet）采用双分支残差架构，将心理先验注入冻结的MDM主干。其核心设计要点如下：

- **冻结主干**：保留预训练MDM的Transformer编码器，确保文本到运动的语义保真度不被破坏。
- **可训练人格分支**：并行构建一个与主干结构相同的人格编码分支，接收OCEAN五维人格向量作为条件输入。
- **零初始化融合**：人格分支的输出通过零初始化线性层与主干特征逐层相加。零初始化确保训练初期残差贡献为零，避免灾难性遗忘，随后逐步学习人格相关的特征偏移。

这种残差注入策略的关键优势在于：人格条件不是粗暴地与文本嵌入求和或投影到噪声运动上，而是作为主干特征的精细化调制信号，使模型能够学习“同一语义下不同人格的运动学差异”。

### 运动精化：Laban-Gd

Laban-Gd（Laban Guidance）在扩散采样的后期阶段，利用拉班运动分析（LMA）的分析梯度对关节旋转进行物理级精化。其工作流程如下：

**1. 人格到Laban Effort的映射（OCEAN-LE）**

首先通过标准化Personality-Effort矩阵（NPE，引自Durupinar等人的用户研究）将OCEAN人格向量映射为四个Laban Effort因子（Space、Weight、Time、Flow）。对于Effort因子 $i$，其正、负贡献分别定义为：

$$E_{i}^{+} = \max(NPE(i, j) \cdot \mathbf{P}(j)) \quad | \quad NPE(i, j) \cdot \mathbf{P}(j) > 0$$

$$E_{i}^{-} = \min(NPE(i, j) \cdot \mathbf{P}(j)) \quad | \quad NPE(i, j) \cdot \mathbf{P}(j) < 0$$

Effort因子的总值为：$E_{i} = E_{i}^{+} + E_{i}^{-}$，其中 $i \in (1, 4)$ 对应四个Effort维度，$j \in (1, 5)$ 对应OCEAN五维度。

**2. 目标关节旋转的确定**

基于Effort因子的符号，PCMG专注于**Space**和**Weight**两个Effort维度，通过预定义的旋转符号表（Table I和Table II）确定各关节的目标旋转方向。例如，间接Space（Space为负）对应特定关节的内旋/外旋模式，轻Weight（Weight为负）对应另一组关节的旋转约束。

**3. 采样过程中的梯度引导**

在扩散采样的后期步骤（$t < T_G$，即运动已基本成形时），对预测均值 $\pmb{\mu}_t$ 施加分析梯度引导：

$$\pmb{\mu}_{t} = \pmb{\mu}_{t} - \tau \nabla_{\pmb{\mu}_{t}} G(\pmb{\mu}_{t}, \pmb{c}^{p})$$

其中 $\tau$ 为引导强度，差异函数 $G$ 定义为：

$$G(\pmb{\mu}, \pmb{c}^{p}) = \frac{\sum_{n}\sum_{j} \sigma_{nj} \left\| \pmb{c}^{p} - \pmb{R}(\pmb{\mu}) \right\|_{2}}{\sum_{n}\sum_{j} \sigma_{nj}}$$

这里 $\pmb{R}(\pmb{\mu})$ 将去噪后的相对运动表示转换为全局坐标，$\pmb{c}^{p}$ 为人格一致的目标关节坐标，$\sigma_{nj}$ 为二进制掩码，指示第 $n$ 帧第 $j$ 个关节是否受当前Effort因子影响。$G$ 本质上是受影响关节的加权L2距离，通过梯度下降使生成的运动在关节旋转层面逼近人格目标。

**4. 延迟引导策略**

Laban-Gd仅在 $t < T_G$ 时激活。早期扩散步骤中样本噪声较大，强行施加引导会导致脚步滑动等物理失真；而在运动轮廓清晰后再进行精化，可在物理可信度和个性鲜明度之间取得平衡。

### 关键设计决策的证据

消融实验（Table IV）表明：移除OCEAN-CN导致FID从3.7754升至6.0288（+37.38%），PRS从0.6535降至0.3413，验证了个性整合对运动真实感和个性表达的双重必要性。移除Laban-Gd则使PRS从0.6535降至0.6086，用户研究中73.64%的参与者偏好完整模型，证实了分析性引导对精细个性运动学细节的贡献。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/002_Figure_2.jpg]]
*Figure 2: (a) Personality integration with OCEAN-CN. PCMG generates motions from text prompt p, personality traits c and noisy motion sequence xt, predicting the clean motion x0. (b) Kinematic refinement with Laban-Gd. During sampling, PCMG first performs coarse denoising from t { = } T to $\scriptstyle$ t = $T _ { G }$ then uses Laban-Gd to refine µt before sampling xt−1, yielding the final motion x0*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/003_Figure_3.jpg]]
*Figure 3: Detailed illustration of our proposed Laban-Gd module. Laban-Gd adjusts the generated motions based on personality, highlighting the differences exhibited by individuals with various personalities*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/008_Figure_5.jpg]]
*Figure 5: Visual comparisons of the ablation designs and our full model. The red rectangles highlight issues such as unnatural movements, in contrast to the more realistic results highlighted in green. -1 indicates a lower trait level on a personality dimension, while 1 represents a higher trait level*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/013_Figure_2.jpg]]
*Figure 2: Motion realism scores across the five dimensions of the OCEAN model*



## 实验与关键发现

### 主实验结果

PCMG在MoOCEAN数据集上对所有基线方法取得了全面的领先。**TABLE III**报告了核心定量结果：完整模型在运动真实感指标FID上达到**3.7754**，相比最强基线MotionDiffuse+Personality的5.4670降低了**30.9%**，相比朴素注入基线MDM+Personality的5.7534降低了**34.4%**。语义匹配精度同样显著提升，R-precision（Top-3）从MDM+Personality的0.2656提升至**0.3281**。最关键的人格表达指标PRS（Personality Recognition Score）达到**0.6535**，远超MotionDiffuse+Personality的0.4877（提升**34.0%**），表明生成动作的人格可区分性大幅增强。物理可信度方面，完整模型的脚部滑动率FSR为0.1380，与基线基本持平或略优。运动多样性Diversity达到5.6979，接近真实数据的分布范围，未出现模式坍塌。

定性结果（**Fig. 4**）进一步验证了上述优势：基线方法（MDM+Personality、MDM+LLM、MotionDiffuse+Personality）在语义正确时往往产生缺乏人格特征的中性动作，或出现不自然的关节姿态（图中红色矩形标注）；PCMG生成的动作为语义一致且人格鲜明（绿色矩形标注），例如高外向性个体的动作幅度更大、空间利用更广，而高神经质个体则呈现更拘谨的运动模式。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison. Our approach generates motions that are more consistent with text and personality conditions, as well as physically more plausible, compared to the baselines. The red rectangles on the baseline methods highlight issues such as unnatural motions, in contrast to the more realistic results marked by the green rectangles. -1 indicates a lower level of trait on a personality dimension, while 1 represents a higher level of trait*

### 消融实验

**TABLE IV**的消融研究揭示了两个核心模块的独立贡献：

- **移除OCEAN-CN**：FID从3.7754急剧上升至6.0288（**+37.38%**），PRS从0.6535骤降至0.3413，几乎丧失人格表达能力。这表明OCEAN-CN的残差注入架构不仅是人格信息传递的关键通道，还对维持运动真实感至关重要——冻结MDM主干配合零初始化融合层有效避免了灾难性遗忘。

- **移除Laban-Gd**：PRS从0.6535降至0.6086，FID从3.7754升至4.1031。虽然降幅小于移除OCEAN-CN，但人格匹配度的退化证实了LMA分析梯度引导对精细运动学细节的贡献。值得注意的是，仅靠扩散模型的特征层融合无法完全捕捉人格在关节旋转层面的物理表现，Laban-Gd在采样后期的引导弥补了这一缺口。

**Appendix Table I**进一步消融了人格条件的注入策略。将人格向量与文本嵌入直接求和再与噪声运动拼接的策略表现最差（FID=5.9423），而PCMG采用的“人格条件直接加在噪声运动上、再拼接文本嵌入”的方案效果最优（FID=3.7754）。这暗示人格信息更适合作为运动先验注入输入空间，而非与语义条件混合。

### 用户研究

**Appendix Table II**的用户研究（22名参与者）显示，**73.64%**的参与者偏好完整模型生成的动作而非移除Laban-Gd的变体，确认了分析引导对人格表达的主观可感知性。**Fig. 6**进一步从人格匹配度和运动真实感两个维度评估：完整模型在两个维度上均获得最高偏好分。

### 失败模式与局限

尽管整体性能优异，实验中暴露出几个值得关注的边界情况：

1. **脚部滑动的轻微增加**：完整模型的FSR（0.1380）虽优于多数基线，但Laban-Gd在增强人格表达时可能引入额外的关节旋转调整，导致少数样本的脚部接触约束被破坏。这是物理可信度与个性鲜明度之间的内在张力。

2. **低显著性人格维度的提升有限**：**Appendix Fig. 2**显示，模型在外向性（Extraversion）和开放性（Openness）维度上的运动真实感评分提升显著，但在宜人性（Agreeableness）和神经质（Neuroticism）维度上提升较小。这与这些维度对应的运动学线索本身较弱、更依赖细微的面部表情或社交上下文有关，纯骨骼运动难以充分表达。

3. **PRS评估的闭环依赖**：PRS依赖一个预训练的运动-人格分类器，该分类器自身的准确率上限限制了评估的可靠性。当分类器对某些人格维度的判别能力较弱时，PRS可能低估或高估真实的个性表达质量。

4. **用户研究样本量限制**：22人的样本规模较小，且主观评分存在个体差异，结论的统计显著性需要更大规模验证。

5. **数据集人格分布不均衡**：MoOCEAN数据集继承自Inter-X，某些人格维度（尤其是极端值）的样本可能不足，影响模型在罕见人格组合上的泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/004_Table.jpg]]
*Table: I THE SPACE EFFORT ROTATION SIGNS. SPACE - MEANS INDIRECT SPACE. TABLE II THE WEIGHT EFFORT ROTATION SIGNS. WEIGHT - MEANS LIGHT WEIGHT*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/005_Table.jpg]]
*Table: III QUANTITATIVE RESULTS ON THE MOOCEAN DATASET. COMPARISON WITH BASELINE METHODS ON MOTION GENERATION*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/007_Table.jpg]]
*Table: IV ABLATION STUDIES ON THE MOOCEAN DATASET*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/011_Table.jpg]]
*Table: I ABLATION STUDIES ON DIFFERENT INTEGRATION STRATEGIES*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/012_Table.jpg]]
*Table: II USER STUDY OF THE EFFECTIVENESS OF LABAN-GD*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2505_22637/figures/009_Figure_6.jpg]]
*Figure 6: User Study on two evaluation dimensions: personality matching and motion realism*



## 定位与知识库关联

### 核心问题定位

现有文本到运动生成方法的核心瓶颈在于：它们主要关注语义保真度，却缺乏显式机制确保生成的动作与目标人格之间的心理一致性。简单的文本描述或黑盒风格编码无法捕捉人格的精细运动学特征，导致动作语义正确但缺乏可区分的个性。PCMG 正是针对这一空白，将人格注入解耦为两个阶段——个性整合与运动精化——从而在保持语义准确性的同时显式地表达人格特质。

### 与基线方法的关系

PCMG 的设计直接回应了三类朴素基线的失败模式：

- **MDM+Personality**：将 OCEAN 人格向量线性投影后直接加到噪声运动中。这种粗暴注入破坏了 MDM 主干（Tevet et al., ICCV 2023）的语义保真度，且无法捕捉人格与运动的非线性耦合关系。PCMG 的 OCEAN-CN 模块以残差方式注入人格特征，并通过零初始化层避免灾难性遗忘，从根本上解决了这一问题。

- **MDM+LLM**：使用 LLM 重写输入文本以反映人格，再用 MDM 生成。该策略将人格表达完全外包给文本工程，无法控制运动学层面的精细差异（如关节旋转幅度、空间使用模式）。PCMG 的 Laban-Gd 模块直接在运动空间通过 LMA 分析梯度进行精化，弥补了这一缺陷。

- **MotionDiffuse+Personality**：在 MotionDiffuse（Zhang et al., 2023）中直接将人格向量注入动作隐空间。虽然后者提供了更灵活的条件注入机制，但依然缺乏对人格-运动关联的物理约束。PCMG 的 Laban-Gd 通过可微的 LMA 能量函数引入心理物理先验，使生成动作在关节层面符合人格预期。

消融实验量化了各组件的贡献：移除 OCEAN-CN 导致 FID 从 3.7754 升至 6.0288（+37.38%），PRS 从 0.6535 降至 0.3413，表明个性整合对运动真实感和个性表达至关重要；移除 Laban-Gd 则使 PRS 降至 0.6086，说明分析性引导对精细个性运动学细节有显著贡献。附录中的集成策略消融进一步表明，将人格条件直接加在噪声运动上再拼接文本嵌入的效果最优，而将人格和文本嵌入直接求和的策略性能不佳（FID 5.9423 vs 3.7754）。

### 适用边界

PCMG 的有效性建立在以下前提之上：

1. **人格标注的存在**：模型依赖 OCEAN 五维人格向量作为条件输入，需要数据集提供明确的人格标签。当前仅在 MoOCEAN 数据集上验证，该数据集从 Inter-X 转换而来，通过 LLM 将双人交互描述转为单人提示并标准化骨骼格式。

2. **扩散模型的采样机制**：Laban-Gd 的引导仅在扩散采样后期（t < T_G）生效，因为早期样本噪声过大，强引导可能引起脚步滑动等不自然现象。这意味着 Laban-Gd 的效果依赖于扩散模型的采样质量。

3. **LMA 因素的覆盖范围**：当前 Laban-Gd 仅关注 Space 和 Weight 两个 Effort 因素，通过预定义的关节旋转符号表进行引导。对于 Time 和 Flow 因素，以及更复杂的身体部位约束，尚未纳入精化范围。

4. **人格维度的可区分性**：模型在 Extraversion 等高显著性维度上提升明显，但在 Agreeableness、Neuroticism 等维度上提升较小，因为这些维度对应的运动线索较弱，LMA 映射的区分度有限。

### 局限与开放问题

**已识别的局限**：

- **数据分布偏差**：MoOCEAN 数据集的人格分布可能仍存在不平衡，个别维度样本较少，影响模型在罕见人格上的泛化。论文未提供各维度样本量的详细分布。

- **评估指标的依赖**：PRS 依赖一个训练好的运动-人格分类器，该分类器自身的准确率限制了评估的可靠性。分类器的架构和训练细节未在正文中充分披露。

- **物理可信度与个性鲜明度的权衡**：Laban-Gd 在增强人格表达时可能会轻微增加脚步滑动（FSR 略高于基线），需要在物理可信度和个性鲜明度之间权衡。

- **用户研究规模**：用户研究仅招募 22 人，样本量小且存在主观偏差，结论的统计显著性有待扩大验证。

**开放问题**：

1. 如何构造更均衡且覆盖全人格谱系的数据集，以减少人格不平衡带来的偏差？
2. 能否设计更客观的人格匹配度量标准，降低对分类器的依赖？
3. Laban-Gd 中的引导强度 τ 和启动时间 T_G 的最优选择策略及其对生成质量的影响是什么？
4. 是否可以将该框架扩展到多人物交互场景，同时保持每个人的独立人格表现？
5. 如何提升对低显著性人格维度（如 Agreeableness、Neuroticism）的运动学精细控制，例如通过引入更复杂的身体部位约束或扩展 LMA 因素覆盖范围？



## 原文 PDF

![[paperPDFs/arxiv_2025/PCMG_Psychology_driven_Personality_consistent_Text_to_Motion_Generation.pdf]]
