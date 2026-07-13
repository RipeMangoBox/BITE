---
title: "Motion Anything: Any to Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Motion_Anything_Any_to_Motion_Generation.pdf
project_link: "https://steve-zeyu-zhang.github.io/MotionAnything"
code_link: null
aliases:
- MA
- MAAMG
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过条件引导的注意力掩码策略，动态选择时间关键帧与空间关键动作进行遮蔽与恢复，实现多模态对齐。
primary_logic: 利用注意力分数作为条件-运动相关性度量，对高注意力区域进行掩码，强制模型学习条件与运动间的对应关系；同时自适应切换自注意力和交叉注意力处理不同模态条件。
claims:
- 基于注意力的掩码在 HumanML3D 上 FID 达到 0.028，显著优于随机掩码(0.049)等策略
- Motion Anything 在 HumanML3D 上 FID 相比 MoGenTS 改善约 15%
- 多模态条件（文本+音乐）在 TMD 上 FID_k 21.46 优于单条件 25.07，验证多模态对齐提升
- Temporal Adaptive Transformer 的自注意力模式在文本到动作中优于跨注意力，R Precision Top1 0.546 vs 0.535
---

# Motion Anything: Any to Motion Generation

> [!tip] 核心洞察
> 利用注意力分数作为条件-运动相关性度量，对高注意力区域进行掩码，强制模型学习条件与运动间的对应关系；同时自适应切换自注意力和交叉注意力处理不同模态条件。

| 字段 | 内容 |
|------|------|
| 中文题名 | Motion Anything：任意条件到人体动作生成 |
| 英文题名 | Motion Anything: Any to Motion Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2503.06955) · [Project](https://steve-zeyu-zhang.github.io/MotionAnything) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Motion Anything |
| Dataset | HumanML3D, KIT-ML, AIST++, TMD |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.028 vs MoGenTS 0.033 (-0.005 (~15% relative))；R Precision Top1↑ 0.546 vs MoGenTS 0.529 (+0.017)。
> - KIT-ML 上，FID↓ 0.131 vs MoGenTS 0.143 (-0.012)。
> - AIST++ 上，FID_g↓ (motion quality) 8.56 vs UDE 8.69 (-0.13)。

## 概要

现有掩码自回归动作生成方法存在两个关键瓶颈：一是采用随机掩码策略，无法根据条件自适应关注动作序列中的关键动态帧与关键身体部位；二是多数方法仅支持单一模态条件或简单的嵌入拼接，难以有效整合多模态信息进行可控生成。这导致生成动作与条件语义的对齐精度不足，可控性受限。

Motion Anything 提出一种**任意条件到人体动作生成**框架，核心机制是基于注意力的掩码建模（Attention-based Mask Modeling）。该方法利用条件与动作之间的注意力分数作为相关性度量，在时间维度和空间维度上自适应地选择高注意力区域进行掩码，迫使模型学习条件与运动之间的细粒度对应关系。同时，通过时序自适应 Transformer（Temporal Adaptive Transformer, TAT）和空间对齐 Transformer（Spatial Aligning Transformer, SAT），模型可根据条件模态动态切换自注意力与交叉注意力，实现多模态条件的有效融合。

主要实验结果如下（详见 Table 2–4）：

- **文本到动作**：在 HumanML3D 上 FID 达到 0.028，R Precision Top1 达到 0.546，相比 MoGenTS 分别相对改善约 15% 和 1.7 个百分点；在 KIT-ML 上 FID 为 0.131，同样优于现有方法。
- **音乐到舞蹈**：在 AIST++ 上 FID_g 达到 8.56，Beat Align Score 为 0.2757，均取得最优或次优结果。
- **文本+音乐到舞蹈**：在 TMD 数据集上 FID_k 为 21.46，MMDist 为 5.34，显著优于 TM2D 和 MotionCraft 等基线，验证了多模态条件整合的有效性。

消融实验进一步证实：基于注意力的掩码策略（FID 0.028）明显优于随机掩码（0.049）及 KMeans、GMM、置信度、密度等替代策略；掩码比率在 30% 附近性能最优且方法对比率变化具有鲁棒性；TAT 在文本到动作任务中使用自注意力优于跨注意力；多模态条件（文本+音乐）相比单模态条件在 TMD 上 FID_k 从 25.07 降至 21.46，提升显著。



### 问题域：从条件到人体动作的生成

人体动作生成旨在根据给定的控制信号（如文本描述、音乐节拍或两者的组合）合成自然、多样的人体运动序列。该任务在动画制作、虚拟人交互、游戏开发等领域具有广泛应用。近年来，扩散模型和掩码自回归方法在该领域取得了显著进展，但一个核心瓶颈始终存在：**现有方法难以根据条件信号自适应地关注动作序列中的关键动态帧和关键身体部位**。

### 现有方法的结构性缺陷

当前主流的掩码自回归方法（如 **MoMask**、**BAMM**）采用随机掩码策略，在训练过程中随机遮蔽运动标记，迫使模型学习从可见部分恢复完整序列。这种策略存在两个根本性局限：

1. **无差别掩码**：随机掩码平等对待所有帧和所有身体关节，无法区分哪些时间片段或空间部位对条件信号更为关键。例如，在文本“一个人挥动右手”中，右手和挥动的时间段应当被重点建模，但随机掩码无法体现这种条件-运动的对应关系。

2. **单模态条件融合薄弱**：现有方法通常仅支持单一条件模态（纯文本或纯音乐），或通过简单的嵌入拼接处理多模态输入。这导致模型无法有效利用多模态条件之间的互补信息，限制了生成动作的可控性和对齐精度。Table 1 的方法对比表明，无论是单任务模型还是多任务模型，每次只能处理一种条件，忽视了多模态整合对于更可控生成的重要性。

### 核心动机：条件引导的注意力掩码

针对上述瓶颈，本文的核心动机是：**利用注意力分数作为条件与运动之间相关性的度量，对高注意力区域进行掩码，强制模型学习条件与运动间的精确对应关系**。这一思路的直觉在于：如果模型在推理时对某个时间帧或某个身体部位给予了高注意力，说明该区域与条件信号高度相关；在训练中主动遮蔽这些高相关区域，可以迫使模型更深入地理解条件语义，从而提升生成动作的质量和对齐精度。

此外，不同模态的条件（文本 vs. 音乐）具有不同的语义结构——文本描述通常指向具体的身体部位和动作类型，而音乐节拍更多约束动作的节奏和风格。因此，模型需要**自适应地切换注意力机制**来处理不同模态的条件，而非采用一刀切的融合方式。这构成了本文设计 Temporal Adaptive Transformer (TAT) 和 Spatial Aligning Transformer (SAT) 的动机基础。

### 目标定位

综上，Motion Anything 旨在构建一个统一的任意条件到动作生成框架，通过注意力引导的时空掩码策略和模态自适应 Transformer 架构，实现对文本、音乐及多模态组合条件的高质量、可控动作生成。



## 核心方法与创新机理

Motion Anything 的核心创新在于用**条件引导的注意力掩码建模**替代了传统掩码自回归方法中的随机掩码，并通过**模态自适应 Transformer** 实现多模态条件的灵活整合。这两个 changed slot 共同解决了现有方法无法根据条件自适应关注关键动态帧和身体部位的瓶颈。

### 从随机掩码到注意力掩码

现有掩码自回归方法（如 **MoMask**）采用随机掩码策略，在动作序列的时空维度上不加区分地遮蔽 token，迫使模型从噪声中重建完整动作。这种策略忽略了条件（文本或音乐）与动作之间的对应关系——并非所有帧和关节对给定的条件同等重要。

Motion Anything 将掩码策略改为**基于注意力的时空选择性掩码**（Figure 2 对比了两种策略的差异）。具体而言，模型首先计算条件嵌入与动作序列之间的注意力分数，然后将高注意力区域识别为“条件-运动相关性”最强的部分，**对这些关键帧和关键身体部位进行掩码**，强制模型学习条件与运动之间的精确对应关系。这一设计的因果逻辑是：如果模型能在高相关性区域被遮蔽后仍准确恢复动作，说明它真正理解了条件语义，而非依赖统计相关性进行表面拟合。

消融实验为这一创新提供了决定性证据（Table 5）：在 HumanML3D 上，注意力掩码的 FID 达到 0.028，显著优于随机掩码（0.049）、KMeans 聚类掩码（0.035）、GMM 掩码（0.038）、置信度掩码（0.042）和密度掩码（0.046）等策略。掩码比率消融（Table 6）进一步显示，时间维度和空间维度各 30% 的掩码比率达到最优，且方法对掩码比率变化具有鲁棒性。

### 模态自适应 Transformer：TAT 与 SAT

多模态条件（文本、音乐、文本+音乐）对动作生成的约束方式本质不同：文本描述通常与动作的整体语义相关，音乐节拍则与动作的时间节奏强耦合。Motion Anything 通过两个协同工作的 Transformer 模块实现模态自适应处理。

**Temporal Adaptive Transformer（TAT）** 负责对齐时间维度的条件与动作。其关键设计在于**根据条件模态动态切换注意力机制**：当条件为文本时，TAT 使用自注意力（self-attention）处理动作序列的时间 token，因为文本语义需要在整个时间轴上建立全局关联；当条件为音乐时，TAT 切换到交叉注意力（cross-attention），将音乐的时间特征（如节拍、强度包络）直接注入动作序列的时间 token。消融实验（Table 7）验证了这一设计的必要性：在文本到动作任务中，自注意力模式的 R Precision Top1 达到 0.546，优于交叉注意力模式的 0.535，说明文本条件下的全局语义建模更为关键。

**Spatial Aligning Transformer（SAT）** 则专注于空间维度的身体部位对齐，始终使用交叉注意力将条件特征映射到身体关节的 token 上，恢复被注意力掩码遮蔽的关键部位动作。

### 多模态条件整合

与 **TM2D**、**MotionCraft** 等方法仅支持单模态条件或简单的嵌入拼接不同，Motion Anything 通过 TAT 的模态自适应切换实现了**同时编码多种模态条件**（Table 1 对比了各方法的多模态能力）。在 TMD 数据集上，文本+音乐双模态条件的 FID_k 达到 21.46，显著优于仅使用音乐的 25.07（Table 8），验证了多模态对齐对生成质量的提升。这一能力使得 Motion Anything 成为首个在统一框架下支持文本到动作、音乐到舞蹈、文本+音乐到舞蹈三种任务的 any-to-motion 方法。



Motion Anything 的整体 pipeline 围绕一个核心思想构建：**通过条件引导的注意力掩码，迫使模型在时空维度上学习条件与运动之间的对应关系**。整个框架由四个主要模块串联而成，形成“编码 → 掩码 → 恢复 → 生成”的闭环。

### 模块关系与数据流

1. **条件编码器（Condition Encoders）**：文本条件通过文本编码器提取嵌入，音频条件通过音频编码器提取嵌入。不同模态的条件被分别编码后，送入后续的掩码与恢复模块（Figure 3(b)）。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/003_Figure_3.jpg]]
*Figure 3: Motion Anything architecture. The multimodal architecture consists of several key components: (a) temporal and (c) spatial attention-based masking, (b) motion generator, and (d) a single block of motion generator. These components enable the model to learn key motions corresponding to the given conditions, and facilitate alignment between multi-modal conditions and motion features*

2. **注意力掩码（Attention-based Masking）**：这是框架的核心创新。给定条件嵌入与初始运动序列，模块计算条件-运动之间的注意力分数，并**在时间和空间两个维度上，对注意力分数高的区域进行掩码**。这意味着模型会主动遮蔽那些与条件最相关的关键帧和关键身体部位动作，迫使后续模块从上下文中恢复这些被遮蔽的信息，从而强化条件-运动的对齐（Section 3.2, Algorithm 1, Figure 4）。

3. **时序自适应 Transformer（Temporal Adaptive Transformer, TAT）**：负责在时间维度上恢复被掩码的关键帧。TAT 的关键设计在于**根据条件模态动态切换注意力机制**：对于文本条件使用自注意力，对于音乐条件使用交叉注意力。这种模态自适应策略使 TAT 能针对不同条件类型，以最优方式对齐时序运动特征（Section 3.2, Algorithm 2）。

4. **空间对齐 Transformer（Spatial Aligning Transformer, SAT）**：负责在空间维度上恢复被掩码的身体部位动作。SAT 统一使用交叉注意力，将条件嵌入与经过 TAT 恢复的运动特征进行空间对齐，补全被遮蔽的身体部位运动（Section 3.2, Algorithm 3）。

5. **运动生成器（Motion Generator）**：整体掩码 Transformer，接收经过 TAT 和 SAT 恢复的运动标记以及条件嵌入，最终生成完整的动作序列。模型配置为 2 层 TAT + 2 层 SAT，总计 12.65M 参数、137.35 GFLOPs（Section 4.2）。

### 与基线方法的关键差异

现有掩码自回归方法（如 **MoMask**）采用随机掩码策略，无法根据条件自适应地关注关键动态帧和身体部位。Motion Anything 将掩码策略从“随机”改为“注意力引导”，并将单一的掩码 Transformer 升级为模态自适应的 TAT + SAT 双阶段架构，从而在多模态条件下实现了更精细的时空可控生成。



Motion Anything 的生成管线由四个核心模块串联构成，其关键创新集中在 **Attention-based Masking** 与两个级联的掩码 Transformer——**Temporal Adaptive Transformer (TAT)** 和 **Spatial Aligning Transformer (SAT)**。以下按数据流顺序拆解各模块的设计逻辑。

### 3.1 条件编码器 (Condition Encoders)

文本条件与音频条件分别通过独立的编码器提取嵌入表示，作为后续掩码策略与恢复 Transformer 的条件信号。文本编码器将自然语言描述映射为语义嵌入，音频编码器提取音乐节拍与风格特征。两种模态的嵌入在进入掩码生成器前已完成对齐，为多模态条件融合提供统一接口（Figure 3b）。

### 3.2 Attention-based Masking

**设计动机**：现有掩码自回归方法（如 MoMask）采用随机掩码策略，无法根据条件自适应关注动作序列中的关键动态帧与身体部位，导致条件-动作对齐弱、可控性差。

**核心机制**：利用条件嵌入与动作序列之间的交叉注意力分数作为“条件-动作相关性”的度量，对高注意力区域进行选择性掩码，迫使模型在恢复阶段学习条件与运动间的对应关系。具体流程如 Algorithm 1 所示：

1. 计算条件嵌入与动作标记之间的注意力分数矩阵。
2. 分别在**时间维度**（关键帧）和**空间维度**（关键身体部位）上选取 Top-K 高注意力区域。
3. 对被选中区域施加掩码，其余区域保持可见。

Figure 4 可视化了该注意力图——高亮区域对应条件语义最相关的动作片段与关节，验证了注意力分数作为掩码引导信号的有效性。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/005_Figure_4.jpg]]
*Figure 4: Attention map. The attention map provides a direct visualization of our attention-based masking approach, which selectively masks regions in the motion sequence with high attention scores*

**与随机掩码的本质区别**：随机掩码均匀丢弃信息，模型无差别地学习全局重建；注意力掩码则聚焦于“条件-动作”耦合最强的区域，本质上是一种**条件感知的课程学习**——先遮蔽最相关的部分，再通过恢复过程强化条件对齐。

### 3.3 Temporal Adaptive Transformer (TAT)

TAT 负责在时间维度上恢复被掩码的关键帧，其核心创新在于**模态自适应注意力机制**（Algorithm 2）：根据输入条件的模态类型，动态切换注意力计算方式。

- **文本到动作**：TAT 使用**自注意力**（Self-Attention），在动作序列的时间标记之间建模长程依赖。消融实验（Table 7）证实，自注意力模式在 R Precision Top1 上达到 0.546，优于跨注意力模式的 0.535，表明文本语义更适合通过动作序列内部的时序一致性来恢复。
- **音乐到动作 / 多模态**：TAT 切换为**跨注意力**（Cross-Attention），将音乐节拍嵌入作为 Query，动作时间标记作为 Key/Value，实现节奏信息与动作帧的直接对齐。

这种自适应切换避免了单一注意力模式在不同模态条件下的失配问题，是模型统一处理“任意条件”的关键设计。

### 3.4 Spatial Aligning Transformer (SAT)

SAT 接收 TAT 恢复后的动作序列，在空间维度上对被掩码的身体部位进行细粒度重建（Algorithm 3）。与 TAT 不同，SAT 固定使用**跨注意力**：以条件嵌入为 Query，空间维度上的身体部位标记为 Key/Value，确保每个关节的动作与全局条件语义保持一致。SAT 的掩码同样由 Attention-based Masking 策略在空间维度上生成，形成“时间恢复 → 空间对齐”的级联结构。

### 3.5 整体架构与参数配置

四个模块的堆叠方式为：条件编码器 → Attention-based Masking（时空两个分支）→ TAT（2 层）→ SAT（2 层），共 4 层掩码 Transformer。模型总参数量 12.65M，计算量 137.35 GFLOPs（Section 4.2）。消融实验（Table 9）表明，层数 N=4 时性能最优，继续增加层数不再带来明显增益。

**注**：本文未提供各模块的显式数学公式（如注意力分数计算、掩码选择函数的具体形式），仅通过算法伪代码描述流程。若需精确公式推导，需查阅原论文补充材料或代码实现。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/002_Figure_2.jpg]]
*Figure 2: Masking strategy comparison. This figure demonstrates the key differences between the previous random masking strategy [21] (top) and our attention-based masking (bottom). Our masking strategy focuses on the more significant and dynamic parts of the motion (colored) corresponding to the condition*



## 实验与关键发现

### 主实验结果

Motion Anything 在三个核心任务（文本到动作、音乐到舞蹈、文本+音乐到舞蹈）上均取得最优或次优结果，验证了注意力掩码策略与多模态自适应架构的有效性。

**文本到动作（HumanML3D / KIT-ML）**。在 HumanML3D 上，Motion Anything 的 FID 达到 0.028，相比最强基线 MoGenTS（0.033）相对改善约 15%；R Precision Top1 达到 0.546，超过 MoGenTS 的 0.529。在 KIT-ML 上，FID 为 0.131，优于 MoGenTS 的 0.143（Table 2）。该增益来源于注意力掩码在时空维度上聚焦条件相关的关键帧和身体部位，而非随机丢弃标记。

**音乐到舞蹈（AIST++）**。Motion Anything 在运动质量指标 FID_g 上达到 8.56，优于 UDE（8.69）；节拍对齐分数 Beat Align Score 为 0.2757，略高于 Bailando++（0.2720）（Table 3）。这表明 Temporal Adaptive Transformer 对音频时序条件的自适应注意力计算能够有效捕捉节拍-动作对应关系。

**文本+音乐到舞蹈（TMD）**。多模态条件下，Motion Anything 的 FID_k 达到 21.46，显著优于 MotionCraft（24.21）和 TM2D（26.02）；多模态距离 MMDist 为 5.34，低于 TM2D（6.13）（Table 4）。注意 TM2D 和 MotionCraft 本身不支持同时接收两种条件模态，实验通过直接组合其条件嵌入来模拟多模态输入以保证公平比较。

### 消融实验

消融实验围绕四个关键设计展开，所有实验均在 HumanML3D 或 TMD 上进行。

**掩码策略对比**。Table 5 对比了注意力掩码与随机掩码、KMeans 聚类掩码、GMM 掩码、置信度掩码、密度掩码等策略。注意力掩码在 FID（0.028）和 R Precision Top1（0.546）上均取得最优，验证了“高注意力区域对应条件-运动相关性”这一核心假设。随机掩码的 FID 为 0.049，差距显著。

**掩码比率**。Table 6 显示，时间掩码比率 T=30%、空间掩码比率 S=30% 时整体性能最优（FID 0.028）。方法对掩码比率变化具有鲁棒性：T 在 20%–40%、S 在 20%–40% 范围内，FID 波动不超过 0.005。

**Temporal Adaptive Transformer 设计**。Table 7 对比了 TAT 中使用自注意力与跨注意力的效果。文本到动作场景下，自注意力模式在 R Precision Top1（0.546 vs 0.535）和 FID（0.028 vs 0.031）上均优于跨注意力，说明文本条件更适合通过自注意力在时序标记间传播条件信息，而非直接与条件嵌入进行跨注意力交互。

**单模态 vs 多模态条件**。Table 8 在 TMD 数据集上表明，文本+音乐双条件（FID_k 21.46）显著优于仅文本（25.07）或仅音乐（24.89）单条件，验证了多模态条件融合对舞蹈生成质量的提升作用。

**模型层数**。Table 9 显示层数 N=4 时达到最佳性能，继续增加层数不再带来明显增益，说明 2 层 TAT + 2 层 SAT 的配置已能充分建模时空条件对齐。

### 失败模式与局限性

论文未报告明确的失败案例或负面结果。以下为基于实验设计的潜在风险点，需人工验证：

- 注意力掩码依赖条件编码器质量：若文本或音频编码器对细粒度语义/节拍信息提取不足，高注意力区域可能错误定位，导致掩码策略失效。
- 多模态条件融合在 TAT 中采用模态自适应切换（自注意力 vs 跨注意力），但该切换规则的具体设计（硬切换或软门控）及其对未见模态组合的泛化能力未充分讨论。
- 所有实验均在标准数据集上进行，对域外条件（如长尾动作描述、非 4/4 拍音乐）的鲁棒性缺乏评估。

### 重要图表结论

- **Table 2**：Motion Anything 在 HumanML3D 和 KIT-ML 上全面超越单任务和多任务基线，多模态方法（蓝色高亮）在运动质量和对齐度上具有系统性优势。
- **Table 3**：音乐到舞蹈任务中，Motion Anything 在运动质量和节拍对齐上达到最优或次优，验证音频条件自适应注意力的有效性。
- **Table 4**：TMD 多模态条件下，Motion Anything 显著领先，说明注意力掩码和模态自适应架构能够有效整合文本语义与音乐节拍信息。
- **Table 5**：注意力掩码在所有掩码策略中表现最优，是方法性能的核心来源。
- **Table 7**：TAT 的自注意力模式优于跨注意力，为文本到动作的条件融合提供了明确的设计指导。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on HumanML3D [19] and KIT-ML [46]. The best and runner-up values are bold and underlined. The right arrow → indicates that closer values to ground truth are better. Multimodal motion generation methods are highlighted in blue*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparison on AIST++ [34]. The best and runner-up values are bold and underlined. Multimodal motion generation methods are highlighted in blue*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/007_Table_4.jpg]]
*Table 4: Quantitative comparison on TMD. The best and runnerup values are bold and underlined*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/012_Table_5.jpg]]
*Table 5: Ablation study of the masking strategy on HumanML3D [19]. The best and runner-up values are bold and underlined. The right arrow → indicates that closer values to ground truth are better*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/014_Table_7.jpg]]
*Table 7: Ablation study of the TAT on HumanML3D [19]. The best values are bold. The right arrow → indicates that closer values to ground truth are better*

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/016_Table_8.jpg]]
*Table 8: Single-modal vs. multimodal generation on TMD dataset*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/013_Table_6.jpg]]
*Table 6: Ablation study of masking ratio on HumanML3D [19]. The best and runner-up values are bold and underlined. The right arrow → indicates that closer values to ground truth are better*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/017_Table_9.jpg]]
*Table 9: Ablation study of number of layers on HumanML3D [19]*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2503_06955/figures/004_Table_1.jpg]]
*Table 1: Methods comparison. Either single-task or multi-task models can handle only one condition at a time, overlooking the importance of integrating multiple modalities for more controllable generation. Our Motion Anything introduces an innovative approach that encodes different modalities simultaneously and adaptively for more controllable generation*



## 定位与知识库关联

### 问题定位：掩码自回归运动的可控性瓶颈

现有掩码自回归运动生成方法面临一个核心瓶颈：随机掩码策略无法根据条件信号自适应地关注运动序列中的关键动态帧和关键身体部位。以 **MoMask** 为代表的随机掩码方案，在训练过程中对所有时间步和关节一视同仁地施加掩码，导致模型难以学习条件与运动细节之间的细粒度对应关系。这一缺陷在多模态条件场景下尤为突出——当条件同时包含文本语义和音乐节拍时，不同模态对应运动的不同时空区域，随机掩码无法区分这些差异化的关联。

Motion Anything 的因果调节变量（causal knob）在于**条件引导的注意力掩码策略**：利用条件编码器与运动序列之间的注意力分数作为相关性度量，对高注意力区域进行选择性掩码，强制模型在恢复被掩码区域时学习条件与运动之间的对应关系。同时，通过模态自适应的 Transformer 设计（Temporal Adaptive Transformer, TAT 和 Spatial Aligning Transformer, SAT），在自注意力和交叉注意力之间动态切换，以处理不同模态条件的对齐需求。

### 方法谱系中的位置

Motion Anything 处于“掩码自回归运动生成”和“多模态条件动作合成”两条技术路线的交汇点。下表梳理了其与代表性基线工作的关系：

| 维度 | 代表性工作 | 核心机制 | Motion Anything 的差异化 |
|------|-----------|---------|------------------------|
| 掩码策略 | **MoMask** (随机掩码) | 对运动 token 随机施加掩码，通过迭代解码恢复 | 基于注意力分数的时空选择性掩码，聚焦条件相关的关键帧和关键关节 |
| 条件融合 | **TM2D** (文本+音乐到舞蹈) | 双模态条件嵌入拼接后输入生成器 | 模态自适应注意力：TAT 根据模态切换自注意力/交叉注意力，SAT 统一使用交叉注意力对齐空间维度 |
| 架构设计 | **MoGenTS** (时空联合建模) | 通用掩码 Transformer 同时处理时空维度 | 解耦为 TAT（时间维度恢复）和 SAT（空间维度恢复），各司其职 |
| 多模态能力 | **MotionCraft** / **LMM** | 多任务学习，但单次推理仅处理一种条件 | 单次推理同时编码多种模态条件，实现 any-to-motion |

从技术演进角度看，Motion Anything 继承了掩码自回归建模（masked autoregressive modeling）的生成范式，但将“掩码”从训练正则化手段升级为**条件对齐的学习机制**。这一思路与注意力引导的数据增强方法有相似之处，但 Motion Anything 将其应用于生成模型的训练阶段，而非数据预处理。

### 适用边界

Motion Anything 的设计假设以下条件成立时性能最优：

1. **条件信号具有明确的时空对应关系**：文本描述通常对应运动的时间阶段（如“先走再跳”），音乐节拍对应动作的节奏变化。如果条件与运动之间缺乏这种结构化的对应（如抽象风格描述），注意力掩码的引导效果可能减弱。
2. **多模态条件互补而非冲突**：当文本和音乐条件指向一致的舞蹈风格时，多模态融合带来增益（Table 8 验证了这一点）；若条件相互矛盾，模型的行为未经验证，需要人工确认。
3. **掩码比率在合理范围内**：消融实验（Table 6）表明 30% 的时空掩码比率最优，方法对该参数具有鲁棒性，但极端比率下的行为未报告。

### 局限与开放问题

**已识别的局限**：

- **长序列生成的连贯性**：论文未提供超过基准数据集典型长度（约 10 秒）的生成结果。注意力掩码依赖条件-运动的局部相关性，长序列中远距离依赖的保持能力未经检验。
- **冲突条件的处理机制**：当多模态条件不一致时（如文本要求“缓慢行走”而音乐节奏急促），模型的行为和生成质量未在消融实验中涉及。
- **计算开销**：注意力掩码需要额外的前向传播计算条件-运动注意力分数，且 TAT 和 SAT 的解耦设计增加了模块数量（模型包含 2 层 TAT + 2 层 SAT，共 12.65M 参数，137.35 GFLOPs）。论文未对比与 MoMask 等轻量方案的推理延迟。

**开放问题**：

1. **注意力掩码的可解释性边界**：Figure 4 可视化了注意力图，但高注意力区域是否确实对应语义相关的运动片段，缺乏定量的人类评估或归因分析。这一机制在失败案例中的表现也未展示。
2. **跨数据集泛化**：实验覆盖 HumanML3D、KIT-ML、AIST++ 和 TMD 四个数据集，但均属于人体动作领域。注意力掩码策略能否迁移到其他序列生成任务（如手势生成、物体运动预测）仍是开放问题。
3. **条件模态的扩展性**：当前支持文本和音频两种模态。扩展到视频、草图或生理信号等条件时，注意力掩码的模态自适应机制需要重新设计 TAT 的注意力切换逻辑，这部分未在论文中讨论。
4. **与扩散模型的对比**：论文仅在掩码自回归框架内进行比较。近年来扩散模型在运动生成中表现强劲，注意力引导的掩码策略与扩散模型的去噪过程是否存在互补性，值得探索。

### 知识库贡献总结

Motion Anything 向运动生成知识库贡献了三个可复用的技术要素：

- **注意力掩码作为条件对齐的通用机制**：不限于特定模态或网络结构，理论上可嵌入任何基于 Transformer 的序列生成模型。
- **模态自适应 Transformer 的设计范式**：TAT 的自注意力/交叉注意力切换逻辑为多模态条件融合提供了轻量级方案，避免了复杂的门控网络或专家混合结构。
- **时空解耦掩码的消融证据**：Table 5–Table 9 的系统消融为后续工作提供了明确的超参数选择参考（30% 掩码比率、4 层网络、文本到动作使用自注意力）。

这些贡献的可靠性受到实验覆盖范围的支撑（四个数据集、多组消融），但在跨任务泛化和长序列场景下的验证仍需后续工作补充。



## 原文 PDF

![[paperPDFs/arxiv_2025/Motion_Anything_Any_to_Motion_Generation.pdf]]
